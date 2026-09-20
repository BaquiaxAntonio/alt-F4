"""
Endpoints FastAPI de la API REST de Educación Guatemala.

Rutas:
  GET  /api/resumen                   → KPIs nacionales
  GET  /api/departamentos             → Lista de 22 departamentos con métricas
  GET  /api/departamento/{nombre}     → Detalle de un departamento
  GET  /api/comparativas              → Urbano vs Rural, Público vs Privado, Hombre vs Mujer
  POST /api/buscar                    → Agente IA (RAG con Claude)
"""
from __future__ import annotations

import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.db.conexion import get_db
from backend.db.models import (
    ResumenDepartamento,
    ResumenSector,
    ResumenSexo,
    ResumenUrbanoRural,
)

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["educacion"])


# ---------------------------------------------------------------------------
# Schemas Pydantic de respuesta
# ---------------------------------------------------------------------------

class KPINacional(BaseModel):
    total_estudiantes: int
    aprobados: int
    no_aprobados: int
    retirados: int
    tasa_aprobacion_promedio: float
    tasa_desercion_promedio: float
    tasa_repitencia_promedio: float
    anio: int


class DepartamentoResumen(BaseModel):
    departamento: str
    total_estudiantes: int
    aprobados: int
    no_aprobados: int
    retirados: int
    tasa_aprobacion: Optional[float]
    tasa_desercion: Optional[float]
    tasa_repitencia: Optional[float]
    porcentaje_publico: Optional[float]
    porcentaje_urbano: Optional[float]
    porcentaje_mujeres: Optional[float]


class ComparativaItem(BaseModel):
    categoria: str
    total_estudiantes: int
    tasa_aprobacion: Optional[float]
    tasa_desercion: Optional[float]
    tasa_repitencia: Optional[float]


class ComparativasResponse(BaseModel):
    tipo: str
    datos: list[ComparativaItem]


class BuscarRequest(BaseModel):
    pregunta: str
    historial: Optional[list[dict]] = None  # Para contexto conversacional (futuro)


class BuscarResponse(BaseModel):
    respuesta: str
    datos_usados: dict
    intenciones_detectadas: list[str]
    confianza: float
    pregunta_original: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_float(value) -> Optional[float]:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# GET /api/resumen → KPIs nacionales
# ---------------------------------------------------------------------------

@router.get("/resumen", response_model=KPINacional, summary="Resumen nacional de indicadores educativos")
def get_resumen(db: Session = Depends(get_db)):
    """
    Retorna los indicadores clave de educación a nivel nacional.
    Fuente: tabla resumen_departamento (agregación de los 22 departamentos).
    """
    sql = text("""
        SELECT
            SUM(total_estudiantes)            AS total,
            SUM(aprobados)                    AS aprobados,
            SUM(no_aprobados)                 AS no_aprobados,
            SUM(retirados)                    AS retirados,
            ROUND(AVG(tasa_aprobacion)::numeric, 2) AS t_aprobacion,
            ROUND(AVG(tasa_desercion)::numeric,  2) AS t_desercion,
            ROUND(AVG(tasa_repitencia)::numeric, 2) AS t_repitencia,
            MAX(anio)                         AS anio
        FROM resumen_departamento
    """)
    row = db.execute(sql).fetchone()
    if row is None or row[0] is None:
        raise HTTPException(status_code=503, detail="Datos aún no disponibles. Ejecuta la ingesta primero.")

    return KPINacional(
        total_estudiantes=int(row[0]),
        aprobados=int(row[1] or 0),
        no_aprobados=int(row[2] or 0),
        retirados=int(row[3] or 0),
        tasa_aprobacion_promedio=_safe_float(row[4]) or 0.0,
        tasa_desercion_promedio=_safe_float(row[5]) or 0.0,
        tasa_repitencia_promedio=_safe_float(row[6]) or 0.0,
        anio=int(row[7] or 2024),
    )


# ---------------------------------------------------------------------------
# GET /api/departamentos → Lista completa con métricas
# ---------------------------------------------------------------------------

@router.get(
    "/departamentos",
    response_model=list[DepartamentoResumen],
    summary="Lista de departamentos con indicadores educativos",
)
def get_departamentos(
    orden: str = Query("tasa_aprobacion", description="Campo para ordenar: tasa_aprobacion, tasa_desercion, tasa_repitencia, total_estudiantes"),
    sector: Optional[str] = Query(None, description="Filtro por sector: Publico, Privado"),
    area: Optional[str] = Query(None, description="Filtro por área: Urbana, Rural"),
    db: Session = Depends(get_db),
):
    """
    Retorna los 22 departamentos de Guatemala con sus indicadores educativos.
    Permite ordenar y filtrar por sector/área.
    """
    columnas_validas = {"tasa_aprobacion", "tasa_desercion", "tasa_repitencia", "total_estudiantes", "departamento"}
    if orden not in columnas_validas:
        raise HTTPException(status_code=400, detail=f"Parámetro 'orden' debe ser uno de: {columnas_validas}")

    # Si hay filtros, se consulta sobre inscripciones (para filtrar por sector/area)
    if sector or area:
        filtros = []
        params: dict[str, Any] = {}
        if sector:
            filtros.append("i.sector ILIKE :sector")
            params["sector"] = f"%{sector}%"
        if area:
            filtros.append("i.area ILIKE :area")
            params["area"] = f"%{area}%"

        where = "WHERE " + " AND ".join(filtros) if filtros else ""
        sql = text(f"""
            SELECT
                i.departamento,
                SUM(i.total_estudiantes)              AS total,
                SUM(i.aprobados)                      AS aprobados,
                SUM(i.no_aprobados)                   AS no_aprobados,
                SUM(i.retirados)                      AS retirados,
                ROUND(
                    100.0 * SUM(i.aprobados) / NULLIF(SUM(i.total_estudiantes), 0), 2
                ) AS tasa_aprobacion,
                ROUND(
                    100.0 * SUM(i.retirados) / NULLIF(SUM(i.total_estudiantes), 0), 2
                ) AS tasa_desercion,
                ROUND(
                    100.0 * SUM(i.no_aprobados) / NULLIF(SUM(i.total_estudiantes), 0), 2
                ) AS tasa_repitencia,
                NULL AS porcentaje_publico,
                NULL AS porcentaje_urbano,
                NULL AS porcentaje_mujeres
            FROM inscripciones i
            {where}
            GROUP BY i.departamento
            ORDER BY tasa_aprobacion DESC NULLS LAST
        """)
        rows = db.execute(sql, params).fetchall()
    else:
        sql = text(f"""
            SELECT
                departamento, total_estudiantes, aprobados, no_aprobados, retirados,
                tasa_aprobacion, tasa_desercion, tasa_repitencia,
                porcentaje_publico, porcentaje_urbano, porcentaje_mujeres
            FROM resumen_departamento
            ORDER BY {orden} DESC NULLS LAST
        """)
        rows = db.execute(sql).fetchall()

    return [
        DepartamentoResumen(
            departamento=r[0],
            total_estudiantes=int(r[1] or 0),
            aprobados=int(r[2] or 0),
            no_aprobados=int(r[3] or 0),
            retirados=int(r[4] or 0),
            tasa_aprobacion=_safe_float(r[5]),
            tasa_desercion=_safe_float(r[6]),
            tasa_repitencia=_safe_float(r[7]),
            porcentaje_publico=_safe_float(r[8]),
            porcentaje_urbano=_safe_float(r[9]),
            porcentaje_mujeres=_safe_float(r[10]),
        )
        for r in rows
    ]


# ---------------------------------------------------------------------------
# GET /api/departamento/{nombre} → Detalle de un departamento
# ---------------------------------------------------------------------------

@router.get(
    "/departamento/{nombre}",
    response_model=dict,
    summary="Detalle completo de un departamento",
)
def get_departamento(nombre: str, db: Session = Depends(get_db)):
    """
    Retorna datos detallados de un departamento incluyendo:
    - Resumen general
    - Desglose por área (urbana/rural)
    - Desglose por sector (público/privado)
    - Desglose por sexo
    """
    # Resumen principal
    depto = db.query(ResumenDepartamento).filter(
        ResumenDepartamento.departamento.ilike(f"%{nombre}%")
    ).first()

    if not depto:
        raise HTTPException(status_code=404, detail=f"Departamento '{nombre}' no encontrado.")

    def desagregacion(columna: str) -> list[dict]:
        sql = text(f"""
            SELECT
                {columna},
                SUM(total_estudiantes) AS total,
                ROUND(100.0 * SUM(aprobados) / NULLIF(SUM(total_estudiantes), 0), 2) AS t_apr,
                ROUND(100.0 * SUM(retirados) / NULLIF(SUM(total_estudiantes), 0), 2) AS t_des
            FROM inscripciones
            WHERE departamento ILIKE :depto
              AND {columna} IS NOT NULL AND {columna} != 'Ignorado'
            GROUP BY {columna}
            ORDER BY total DESC
        """)
        rows = db.execute(sql, {"depto": f"%{nombre}%"}).fetchall()
        return [
            {columna: r[0], "total_estudiantes": int(r[1] or 0),
             "tasa_aprobacion": _safe_float(r[2]), "tasa_desercion": _safe_float(r[3])}
            for r in rows
        ]

    return {
        "departamento": depto.departamento,
        "resumen": {
            "total_estudiantes": depto.total_estudiantes,
            "aprobados": depto.aprobados,
            "no_aprobados": depto.no_aprobados,
            "retirados": depto.retirados,
            "tasa_aprobacion": _safe_float(depto.tasa_aprobacion),
            "tasa_desercion": _safe_float(depto.tasa_desercion),
            "tasa_repitencia": _safe_float(depto.tasa_repitencia),
            "porcentaje_publico": _safe_float(depto.porcentaje_publico),
            "porcentaje_urbano": _safe_float(depto.porcentaje_urbano),
            "porcentaje_mujeres": _safe_float(depto.porcentaje_mujeres),
        },
        "por_area": desagregacion("area"),
        "por_sector": desagregacion("sector"),
        "por_sexo": desagregacion("sexo"),
        "por_nivel": desagregacion("nivel"),
    }


# ---------------------------------------------------------------------------
# GET /api/comparativas → Comparativas temáticas
# ---------------------------------------------------------------------------

@router.get(
    "/comparativas",
    response_model=ComparativasResponse,
    summary="Comparativas temáticas (urbano/rural, público/privado, hombre/mujer)",
)
def get_comparativas(
    tipo: str = Query(
        "urbano_rural",
        description="Tipo de comparativa: 'urbano_rural', 'sector', 'sexo'",
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna comparativas entre categorías.
    - tipo=urbano_rural → Urbana vs Rural
    - tipo=sector → Público vs Privado
    - tipo=sexo → Hombre vs Mujer
    """
    tipo_map = {
        "urbano_rural": (ResumenUrbanoRural, "area"),
        "sector": (ResumenSector, "sector"),
        "sexo": (ResumenSexo, "sexo"),
    }

    if tipo not in tipo_map:
        raise HTTPException(
            status_code=400,
            detail=f"'tipo' debe ser uno de: {list(tipo_map.keys())}",
        )

    Modelo, campo = tipo_map[tipo]
    registros = db.query(Modelo).all()

    if not registros:
        raise HTTPException(status_code=503, detail="Datos no disponibles. Ejecuta la ingesta.")

    datos = [
        ComparativaItem(
            categoria=getattr(r, campo),
            total_estudiantes=r.total_estudiantes,
            tasa_aprobacion=_safe_float(r.tasa_aprobacion),
            tasa_desercion=_safe_float(r.tasa_desercion),
            tasa_repitencia=_safe_float(r.tasa_repitencia),
        )
        for r in registros
    ]

    return ComparativasResponse(tipo=tipo, datos=datos)


# ---------------------------------------------------------------------------
# POST /api/buscar → Agente IA
# ---------------------------------------------------------------------------

@router.post(
    "/buscar",
    response_model=BuscarResponse,
    summary="Consulta al agente de IA (RAG con Claude)",
)
def buscar(body: BuscarRequest, db: Session = Depends(get_db)):
    """
    Agente de análisis educativo impulsado por Claude.

    El agente:
    1. Detecta la intención de la pregunta
    2. Consulta la base de datos con SQL apropiado
    3. Pasa el contexto a Claude
    4. Retorna respuesta en lenguaje natural + datos crudos usados

    La IA nunca inventa cifras: responde solo con datos de la BD.
    """
    from backend.api.agente_ia import query_agente

    pregunta = body.pregunta.strip()
    if not pregunta:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")
    if len(pregunta) > 1000:
        raise HTTPException(status_code=400, detail="La pregunta es demasiado larga (máx 1000 caracteres).")

    log.info("POST /api/buscar: '%s'", pregunta[:80])

    resultado = query_agente(pregunta, db)
    return BuscarResponse(
        respuesta=resultado["respuesta"],
        datos_usados=resultado["datos_usados"],
        intenciones_detectadas=resultado["intenciones_detectadas"],
        confianza=resultado["confianza"],
        pregunta_original=pregunta,
    )


# ---------------------------------------------------------------------------
# GET /api/health → Health check
# ---------------------------------------------------------------------------

@router.get("/health", summary="Health check del backend")
def health_check(db: Session = Depends(get_db)):
    """Verifica que el backend y la base de datos estén operativos."""
    try:
        count = db.execute(text("SELECT COUNT(*) FROM resumen_departamento")).scalar()
        return {
            "status": "ok",
            "departamentos_en_bd": count,
            "mensaje": "Backend operativo" if count else "BD vacía - ejecuta la ingesta",
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error de BD: {str(e)}")
