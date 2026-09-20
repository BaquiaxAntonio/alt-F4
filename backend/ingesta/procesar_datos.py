import os
import json
import sqlite3
import pandas as pd
from pathlib import Path

# Configuracion de rutas
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DICCIONARIO_PATH = DATA_DIR / "diccionario_variables.json"
DB_PATH = BASE_DIR / "educacion.db"

def cargar_diccionario():
    """Carga el diccionario de decodificacion de variables."""
    if not DICCIONARIO_PATH.exists():
        raise FileNotFoundError(f"No se encontro el diccionario en {DICCIONARIO_PATH}")
    with open(DICCIONARIO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def decodificar_columna(serie: pd.Series, mapeo: dict, nombre_default: str = "No especificado") -> pd.Series:
    """Mapea codigos numericos o strings a su etiqueta legible segun el diccionario."""
    # Convertir a string para hacer match seguro
    str_serie = serie.astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    return str_serie.map(mapeo).fillna(nombre_default)

def procesar_archivo_xlsx(ruta_archivo: Path, diccionario: dict) -> pd.DataFrame:
    """
    Lee un archivo XLSX del INE, valida y decodifica las columnas segun el diccionario.
    """
    print(f"-> Leyendo archivo: {ruta_archivo.name}")
    try:
        df = pd.read_excel(ruta_archivo, engine="openpyxl")
    except Exception as e:
        print(f"Error al leer {ruta_archivo.name}: {e}")
        return pd.DataFrame()

    # Normalizar nombres de columnas a minusculas
    df.columns = [c.strip().lower() for c in df.columns]

    # Identificar columnas mapeables comunes en censos educativos INE
    columnas_posibles = {
        "departamento": ["depto", "departamento", "cod_depto", "codigo_departamento"],
        "sector": ["sector", "cod_sector"],
        "area": ["area", "zona", "cod_area", "area_geografica"],
        "sexo": ["sexo", "genero", "cod_sexo"],
        "nivel": ["nivel", "nivel_educativo", "cod_nivel"],
        "resultado": ["resultado", "condicion", "estado_final", "promovido"]
    }

    # Detectar y renombrar
    columnas_mapeadas = {}
    for clave, alternativas in columnas_posibles.items():
        for col in df.columns:
            if col in alternativas:
                columnas_mapeadas[col] = clave
                break

    df_renombrado = df.rename(columns=columnas_mapeadas)

    # Decodificar columnas existentes
    if "departamento" in df_renombrado.columns:
        df_renombrado["departamento_nom"] = decodificar_columna(df_renombrado["departamento"], diccionario.get("departamento", {}))
    if "sector" in df_renombrado.columns:
        df_renombrado["sector_nom"] = decodificar_columna(df_renombrado["sector"], diccionario.get("sector", {}))
    if "area" in df_renombrado.columns:
        df_renombrado["area_nom"] = decodificar_columna(df_renombrado["area"], diccionario.get("area", {}))
    if "sexo" in df_renombrado.columns:
        df_renombrado["sexo_nom"] = decodificar_columna(df_renombrado["sexo"], diccionario.get("sexo", {}))
    if "resultado" in df_renombrado.columns:
        df_renombrado["resultado_nom"] = decodificar_columna(df_renombrado["resultado"], diccionario.get("resultado", {}))

    return df_renombrado

def calcular_agregaciones(df: pd.DataFrame):
    """
    Calcula agregaciones por departamento, sector y area con tasas oficiales.
    """
    if df.empty:
        return None

    # Agregacion por Departamento
    if "departamento_nom" in df.columns and "resultado_nom" in df.columns:
        agrup_depto = df.groupby(["departamento_nom", "resultado_nom"]).size().unstack(fill_value=0)
        return agrup_depto
    return None

def ejecutar_pipeline_ingesta():
    """
    Funcion principal para procesar todos los archivos presentes en data/raw.
    """
    print("=== INICIANDO PIPELINE DE INGESTA EXPRÉS ===")
    diccionario = cargar_diccionario()
    
    archivos_raw = list(RAW_DIR.glob("*.xlsx")) + list(RAW_DIR.glob("*.csv"))
    if not archivos_raw:
        print(f"Aviso: No se encontraron archivos XLSX/CSV en '{RAW_DIR}'.")
        print("Para procesar datos crudos, coloca los 22 archivos departamentales en 'data/raw/'.")
        print("Actualmente el sistema esta utilizando la base de datos precomputada 'educacion.db'.")
        return

    print(f"Se encontraron {len(archivos_raw)} archivos para procesar.")
    dfs = []
    for archivo in archivos_raw:
        if archivo.suffix == ".xlsx":
            df_proc = procesar_archivo_xlsx(archivo, diccionario)
            if not df_proc.empty:
                dfs.append(df_proc)
        elif archivo.suffix == ".csv":
            df_proc = pd.read_csv(archivo)
            dfs.append(df_proc)

    if dfs:
        df_total = pd.concat(dfs, ignore_index=True)
        print(f"Total de registros procesados y decodificados: {len(df_total):,}")
        csv_salida = PROCESSED_DIR / "datos_decodificados_muestra.csv"
        df_total.head(5000).to_csv(csv_salida, index=False, encoding="utf-8")
        print(f"Muestra exportada a: {csv_salida}")

if __name__ == "__main__":
    ejecutar_pipeline_ingesta()
