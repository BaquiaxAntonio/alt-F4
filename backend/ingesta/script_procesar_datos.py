"""
Script de ingesta de datos educativos del INE Guatemala.

Flujo:
  1. Lee archivos XLSX de /data/raw (uno por departamento)
  2. Carga diccionario_variables.json para decodificar códigos → etiquetas
  3. Calcula métricas derivadas (aprobación, deserción, repitencia)
  4. Valida coherencia de los datos
  5. Carga en PostgreSQL (tabla inscripciones)
  6. Genera tablas de resumen agregadas

Uso:
  python -m backend.ingesta.script_procesar_datos
"""
from __future__ import annotations

import json
import logging
import sys
import time
from decimal import Decimal
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

# Añadir raíz del proyecto al path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.db.conexion import SessionLocal, engine
from backend.db.models import (
    Base,
    Inscripcion,
    ResumenDepartamento,
    ResumenSector,
    ResumenSexo,
    ResumenUrbanoRural,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rutas de datos
# ---------------------------------------------------------------------------
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DICT_PATH = DATA_DIR / "diccionario_variables.json"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Año de los datos
ANIO_DATOS = 2024

# Código especial "Ignorado/No aplicable" en el dataset
CODIGO_IGNORADO = 9


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def cargar_diccionario() -> dict[str, dict[str, str]]:
    """Carga el diccionario de variables desde JSON."""
    if not DICT_PATH.exists():
        log.warning(
            "Diccionario no encontrado en %s. Se usará decodificación básica.", DICT_PATH
        )
        return {}
    with open(DICT_PATH, encoding="utf-8") as f:
        return json.load(f)


def decodificar_columna(
    serie: pd.Series,
    mapeo: dict[str, str],
    nombre_columna: str,
) -> pd.Series:
    """
    Convierte códigos numéricos a etiquetas legibles.
    El código CODIGO_IGNORADO se mapea a 'Ignorado'.
    """
    mapeo_local = {int(k): v for k, v in mapeo.items() if k.isdigit()}
    mapeo_local[CODIGO_IGNORADO] = "Ignorado"

    resultado = serie.map(lambda x: mapeo_local.get(int(x), str(x)) if pd.notna(x) else None)
    n_sin_mapear = resultado.isna().sum()
    if n_sin_mapear > 0:
        log.debug("Columna '%s': %d valores sin mapear.", nombre_columna, n_sin_mapear)
    return resultado


def calcular_tasas(
    aprobados: int | float,
    no_aprobados: int | float,
    retirados: int | float,
    total: int | float,
) -> tuple[float | None, float | None, float | None]:
    """
    Calcula tasas de aprobación, deserción y repitencia.
    Retorna None si el total es 0.
    Todas las tasas deben estar en [0, 100].
    """
    if total <= 0:
        return None, None, None

    t_aprobacion = round((aprobados / total) * 100, 2)
    t_desercion = round((retirados / total) * 100, 2)
    t_repitencia = round((no_aprobados / total) * 100, 2)

    # Validación de rango
    for tasa, nombre in [
        (t_aprobacion, "aprobación"),
        (t_desercion, "deserción"),
        (t_repitencia, "repitencia"),
    ]:
        if not (0 <= tasa <= 100):
            log.warning("Tasa de %s fuera de rango: %.2f (total=%d)", nombre, tasa, total)

    return t_aprobacion, t_desercion, t_repitencia


# ---------------------------------------------------------------------------
# Mapeo de columnas del XLSX → nombres internos
# ---------------------------------------------------------------------------

# Ajusta estos nombres según las columnas reales de los XLSX del INE
# (pueden variar; este es el mapeo esperado según la documentación)
COLUMNAS_ESPERADAS = {
    "DEPARTAMENTO": "cod_departamento",
    "MUNICIPIO": "cod_municipio",
    "SECTOR": "cod_sector",
    "AREA": "cod_area",
    "NIVEL": "cod_nivel",
    "GRADO": "cod_grado",
    "SEXO": "cod_sexo",
    "PUEBLO": "cod_pueblo",
    "RESULTADO": "cod_resultado",
    "TOTAL": "total_estudiantes",
    "APROBADOS": "aprobados",
    "NO APROBADOS": "no_aprobados",
    "RETIRADOS": "retirados",
}

# Columnas que necesitan decodificación (columna_xlsx → clave en diccionario)
COLUMNAS_A_DECODIFICAR = {
    "cod_departamento": "DEPARTAMENTO",
    "cod_municipio": "MUNICIPIO",
    "cod_sector": "SECTOR",
    "cod_area": "AREA",
    "cod_nivel": "NIVEL",
    "cod_grado": "GRADO",
    "cod_sexo": "SEXO",
    "cod_pueblo": "PUEBLO",
    "cod_resultado": "RESULTADO",
}


# ---------------------------------------------------------------------------
# Lectura y normalización de un XLSX
# ---------------------------------------------------------------------------

def leer_xlsx(ruta: Path, diccionario: dict) -> pd.DataFrame | None:
    """
    Lee un archivo XLSX del INE, renombra columnas, decodifica y calcula métricas.
    Retorna DataFrame normalizado o None si hay error de esquema.
    """
    log.info("Procesando: %s", ruta.name)
    try:
        df = pd.read_excel(ruta, dtype=str)
    except Exception as e:
        log.error("Error al leer %s: %s", ruta.name, e)
        return None

    # Normalizar encabezados
    df.columns = [c.strip().upper() for c in df.columns]

    # Verificar columnas mínimas
    requeridas = {"TOTAL", "APROBADOS", "NO APROBADOS", "RETIRADOS"}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        # Intento flexible: buscar variantes
        alt_map = {
            "PROMOVIDOS": "APROBADOS",
            "NO PROMOVIDOS": "NO APROBADOS",
            "RETIROS": "RETIRADOS",
        }
        for alt, oficial in alt_map.items():
            if alt in df.columns and oficial not in df.columns:
                df.rename(columns={alt: oficial}, inplace=True)
                faltantes.discard(oficial)

        if faltantes:
            log.warning(
                "Archivo %s: faltan columnas %s. Se omitirá.", ruta.name, faltantes
            )
            return None

    # Renombrar columnas conocidas
    rename_map = {k: v for k, v in COLUMNAS_ESPERADAS.items() if k in df.columns}
    df.rename(columns=rename_map, inplace=True)

    # Convertir numéricos
    for col in ["total_estudiantes", "aprobados", "no_aprobados", "retirados"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Decodificar columnas categoricas
    for col_interno, clave_dict in COLUMNAS_A_DECODIFICAR.items():
        if col_interno in df.columns:
            mapeo = diccionario.get(clave_dict, {})
            df[col_interno] = decodificar_columna(df[col_interno], mapeo, col_interno)

    # Calcular tasas fila por fila
    tasas = df.apply(
        lambda row: calcular_tasas(
            row.get("aprobados", 0),
            row.get("no_aprobados", 0),
            row.get("retirados", 0),
            row.get("total_estudiantes", 0),
        ),
        axis=1,
        result_type="expand",
    )
    df["tasa_aprobacion"] = tasas[0]
    df["tasa_desercion"] = tasas[1]
    df["tasa_repitencia"] = tasas[2]
    df["anio"] = ANIO_DATOS

    log.info("  → %d filas leídas de %s", len(df), ruta.name)
    return df


# ---------------------------------------------------------------------------
# Carga en base de datos
# ---------------------------------------------------------------------------

def guardar_inscripciones(df: pd.DataFrame, db: Session, batch_size: int = 5000):
    """Inserta registros de inscripciones en la BD en batches."""
    total = len(df)
    insertados = 0

    for inicio in range(0, total, batch_size):
        lote = df.iloc[inicio: inicio + batch_size]
        objetos = []
        for _, row in lote.iterrows():
            obj = Inscripcion(
                departamento=row.get("cod_departamento") or "Desconocido",
                municipio=row.get("cod_municipio"),
                sector=row.get("cod_sector"),
                area=row.get("cod_area"),
                zona=row.get("cod_area"),  # Se toma de area si no hay columna zona
                nivel=row.get("cod_nivel"),
                grado=row.get("cod_grado"),
                pueblo=row.get("cod_pueblo"),
                sexo=row.get("cod_sexo"),
                resultado=row.get("cod_resultado"),
                total_estudiantes=int(row.get("total_estudiantes", 0)),
                aprobados=int(row.get("aprobados", 0)),
                no_aprobados=int(row.get("no_aprobados", 0)),
                retirados=int(row.get("retirados", 0)),
                tasa_aprobacion=row.get("tasa_aprobacion"),
                tasa_desercion=row.get("tasa_desercion"),
                tasa_repitencia=row.get("tasa_repitencia"),
                anio=ANIO_DATOS,
            )
            objetos.append(obj)

        db.bulk_save_objects(objetos)
        db.commit()
        insertados += len(lote)
        log.info("  Insertados %d / %d registros...", insertados, total)


# ---------------------------------------------------------------------------
# Cálculo de resúmenes agregados
# ---------------------------------------------------------------------------

def calcular_y_guardar_resumenes(db: Session):
    """Calcula y persiste las tablas de resumen desde inscripciones."""
    log.info("Calculando resumen por departamento...")
    _resumen_departamento(db)

    log.info("Calculando resumen urbano/rural...")
    _resumen_urbano_rural(db)

    log.info("Calculando resumen por sector...")
    _resumen_sector(db)

    log.info("Calculando resumen por sexo...")
    _resumen_sexo(db)


def _agregar(db: Session, columna: str, Modelo, campo_modelo: str):
    """Generic: agrupa inscripciones por columna y guarda en Modelo."""
    from sqlalchemy import text

    sql = text(f"""
        SELECT
            {columna},
            SUM(total_estudiantes) AS total,
            SUM(aprobados)         AS aprobados,
            SUM(no_aprobados)      AS no_aprobados,
            SUM(retirados)         AS retirados
        FROM inscripciones
        WHERE {columna} IS NOT NULL AND {columna} != 'Ignorado'
        GROUP BY {columna}
    """)
    resultado = db.execute(sql).fetchall()

    db.query(Modelo).delete()
    for fila in resultado:
        valor = fila[0]
        total = fila[1] or 0
        aprobados = fila[2] or 0
        no_aprobados = fila[3] or 0
        retirados = fila[4] or 0
        t_apr, t_des, t_rep = calcular_tasas(aprobados, no_aprobados, retirados, total)

        kwargs = {
            campo_modelo: valor,
            "total_estudiantes": total,
            "aprobados": aprobados,
            "no_aprobados": no_aprobados,
            "retirados": retirados,
            "tasa_aprobacion": t_apr,
            "tasa_desercion": t_des,
            "tasa_repitencia": t_rep,
            "anio": ANIO_DATOS,
        }
        db.add(Modelo(**kwargs))
    db.commit()


def _resumen_departamento(db: Session):
    from sqlalchemy import text

    sql = text("""
        SELECT
            departamento,
            SUM(total_estudiantes) AS total,
            SUM(aprobados)         AS aprobados,
            SUM(no_aprobados)      AS no_aprobados,
            SUM(retirados)         AS retirados,
            ROUND(
                100.0 * SUM(CASE WHEN sector = 'Público' THEN total_estudiantes ELSE 0 END)
                / NULLIF(SUM(total_estudiantes), 0), 2
            ) AS pct_publico,
            ROUND(
                100.0 * SUM(CASE WHEN area = 'Urbana' THEN total_estudiantes ELSE 0 END)
                / NULLIF(SUM(total_estudiantes), 0), 2
            ) AS pct_urbano,
            ROUND(
                100.0 * SUM(CASE WHEN sexo = 'Mujer' THEN total_estudiantes ELSE 0 END)
                / NULLIF(SUM(total_estudiantes), 0), 2
            ) AS pct_mujeres
        FROM inscripciones
        WHERE departamento IS NOT NULL AND departamento != 'Ignorado'
        GROUP BY departamento
        ORDER BY departamento
    """)
    resultado = db.execute(sql).fetchall()

    db.query(ResumenDepartamento).delete()
    for f in resultado:
        depto, total, aprobados, no_aprobados, retirados, pct_pub, pct_urb, pct_muj = f
        t_apr, t_des, t_rep = calcular_tasas(aprobados, no_aprobados, retirados, total or 0)
        db.add(ResumenDepartamento(
            departamento=depto,
            total_estudiantes=total or 0,
            aprobados=aprobados or 0,
            no_aprobados=no_aprobados or 0,
            retirados=retirados or 0,
            tasa_aprobacion=t_apr,
            tasa_desercion=t_des,
            tasa_repitencia=t_rep,
            porcentaje_publico=pct_pub,
            porcentaje_urbano=pct_urb,
            porcentaje_mujeres=pct_muj,
            anio=ANIO_DATOS,
        ))
    db.commit()
    log.info("  → %d departamentos procesados.", len(resultado))


def _resumen_urbano_rural(db: Session):
    _agregar(db, "area", ResumenUrbanoRural, "area")
    log.info("  → Resumen urbano/rural guardado.")


def _resumen_sector(db: Session):
    _agregar(db, "sector", ResumenSector, "sector")
    log.info("  → Resumen por sector guardado.")


def _resumen_sexo(db: Session):
    _agregar(db, "sexo", ResumenSexo, "sexo")
    log.info("  → Resumen por sexo guardado.")


# ---------------------------------------------------------------------------
# Validaciones post-ingesta
# ---------------------------------------------------------------------------

def validar_ingesta(db: Session) -> dict[str, Any]:
    """
    Ejecuta checks de integridad y retorna reporte de validación.
    """
    from sqlalchemy import text

    report: dict[str, Any] = {}

    # 1. Total de registros
    total = db.execute(text("SELECT COUNT(*) FROM inscripciones")).scalar()
    report["total_registros"] = total
    log.info("[VALIDACIÓN] Total registros en BD: %d", total)

    # 2. Suma de estudiantes
    suma = db.execute(text("SELECT SUM(total_estudiantes) FROM inscripciones")).scalar() or 0
    report["suma_total_estudiantes"] = int(suma)
    log.info("[VALIDACIÓN] Suma total estudiantes: %d", int(suma))

    # 3. Tasas en rango [0, 100]
    fuera_rango = db.execute(text("""
        SELECT COUNT(*) FROM inscripciones
        WHERE tasa_aprobacion < 0 OR tasa_aprobacion > 100
           OR tasa_desercion  < 0 OR tasa_desercion  > 100
           OR tasa_repitencia < 0 OR tasa_repitencia > 100
    """)).scalar()
    report["tasas_fuera_rango"] = fuera_rango
    if fuera_rango > 0:
        log.warning("[VALIDACIÓN] %d registros con tasas fuera de [0, 100]", fuera_rango)
    else:
        log.info("[VALIDACIÓN] Todas las tasas en rango [0, 100] ✓")

    # 4. Cierre de números: (aprobados + no_aprobados + retirados) <= total
    desfase = db.execute(text("""
        SELECT COUNT(*) FROM inscripciones
        WHERE (aprobados + no_aprobados + retirados) > total_estudiantes
    """)).scalar()
    report["registros_con_desfase"] = desfase
    if desfase > 0:
        log.warning("[VALIDACIÓN] %d registros donde suma > total (posible desfase)", desfase)
    else:
        log.info("[VALIDACIÓN] Cierre de números correcto ✓")

    return report


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def run_ingesta(limpiar_antes: bool = True):
    """
    Ejecuta el pipeline completo de ingesta.

    Args:
        limpiar_antes: Si True, borra inscripciones existentes antes de insertar
    """
    inicio = time.time()
    diccionario = cargar_diccionario()

    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    archivos = sorted(RAW_DIR.glob("*.xlsx")) + sorted(RAW_DIR.glob("*.XLSX"))
    if not archivos:
        log.error("No se encontraron archivos XLSX en %s", RAW_DIR)
        log.info("Por favor coloca los archivos del INE en: %s", RAW_DIR)
        return

    log.info("Se encontraron %d archivos XLSX.", len(archivos))

    db = SessionLocal()
    try:
        if limpiar_antes:
            log.info("Limpiando inscripciones anteriores...")
            db.query(Inscripcion).delete()
            db.commit()

        total_df_list = []
        for ruta in archivos:
            df = leer_xlsx(ruta, diccionario)
            if df is not None and not df.empty:
                total_df_list.append(df)

        if not total_df_list:
            log.error("Ningún archivo se procesó correctamente.")
            return

        df_total = pd.concat(total_df_list, ignore_index=True)
        log.info("Total de filas a insertar: %d", len(df_total))

        # Guardar muestra para diagnóstico
        muestra = df_total.sample(min(100, len(df_total)))
        muestra.to_csv(PROCESSED_DIR / "muestra_decodificada.csv", index=False)
        log.info("Muestra guardada en data/processed/muestra_decodificada.csv")

        # Insertar en BD
        guardar_inscripciones(df_total, db)

        # Calcular resúmenes
        calcular_y_guardar_resumenes(db)

        # Validar
        reporte = validar_ingesta(db)

        # Guardar reporte
        reporte_path = PROCESSED_DIR / "VALIDACION_INGESTA.txt"
        with open(reporte_path, "w", encoding="utf-8") as f:
            f.write("===== REPORTE DE VALIDACIÓN DE INGESTA =====\n\n")
            for k, v in reporte.items():
                f.write(f"{k}: {v}\n")
            f.write(f"\nTiempo total: {time.time() - inicio:.1f}s\n")

        log.info(
            "Ingesta completada en %.1f segundos. Reporte: %s",
            time.time() - inicio,
            reporte_path,
        )

    finally:
        db.close()


if __name__ == "__main__":
    run_ingesta()
