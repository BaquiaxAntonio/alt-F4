"""
Agente IA con patrón RAG (Retrieval-Augmented Generation).

Flujo:
  1. Recibe pregunta del usuario
  2. Clasifica la intención (aprobación, deserción, sector, etc.)
  3. Ejecuta SQL apropiado en PostgreSQL
  4. Construye prompt con contexto real
  5. Llama a Claude API
  6. Retorna respuesta + datos usados + nivel de confianza
"""
from __future__ import annotations

import logging
import os
from typing import Any

import anthropic
from sqlalchemy import text
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuración del cliente Claude
# ---------------------------------------------------------------------------

def _get_claude_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY no está configurada. "
            "Revisa tu archivo .env"
        )
    return anthropic.Anthropic(api_key=api_key)


SYSTEM_PROMPT = """Eres un asistente experto en análisis de datos educativos de Guatemala.
Tu única fuente de información son los datos del INE (Instituto Nacional de Estadística)
sobre educación formal 2024, que te proporcionaré como contexto en cada consulta.

REGLAS ESTRICTAS:
1. Responde ÚNICAMENTE con información de los datos proporcionados.
2. Si no tienes datos para responder, di exactamente: "No tenemos información sobre eso en los datos disponibles."
3. NUNCA inventes cifras, porcentajes o tendencias.
4. Cuando cites un número, menciona de dónde viene (ej: "según los datos de inscripciones 2024").
5. Sé conciso pero informativo. Máximo 3-4 párrafos.
6. Usa lenguaje accesible (la audiencia puede no ser experta en estadística).
7. Si los datos permiten una conclusión relevante (ej: inequidad, necesidad de política), menciónala.

Contexto disponible: datos de 4.3M inscripciones, 22 departamentos, tasas de aprobación, deserción y repitencia."""


# ---------------------------------------------------------------------------
# Clasificación de intención
# ---------------------------------------------------------------------------

INTENT_KEYWORDS: dict[str, list[str]] = {
    "aprobacion": ["aprobaci", "promov", "aprueb", "exitoso", "éxito", "pasan"],
    "desercion": ["deserci", "abandon", "retir", "dejan", "expulsad"],
    "repitencia": ["repitencia", "repiten", "repiti", "doble año"],
    "urbano_rural": ["urban", "rural", "campo", "ciudad"],
    "sector": ["públic", "privad", "sector", "estatal", "subvencion"],
    "sexo": ["hombre", "mujer", "sexo", "género", "niña", "niño", "masculin", "femenin", "brecha"],
    "departamento": ["departamento", "región", "zona geográfica"],
    "pueblo": ["pueblo", "indigen", "maya", "garif", "xinca", "ladino", "mestiz"],
    "nivel": ["primaria", "básico", "diversificad", "nivel", "grado", "preescolar", "párvulo"],
    "nacional": ["nacional", "todo el país", "total", "promedio general", "global"],
}

def clasificar_intencion(pregunta: str) -> list[str]:
    """Detecta los temas de la pregunta para construir la query SQL."""
    pregunta_lower = pregunta.lower()
    intenciones = []
    for intencion, palabras in INTENT_KEYWORDS.items():
        if any(p in pregunta_lower for p in palabras):
            intenciones.append(intencion)
    return intenciones or ["nacional"]


# ---------------------------------------------------------------------------
# Construcción de queries SQL por intención
# ---------------------------------------------------------------------------

def _query_nacional(db: Session) -> dict[str, Any]:
    sql = text("""
        SELECT
            SUM(total_estudiantes) AS total,
            SUM(aprobados)         AS aprobados,
            SUM(no_aprobados)      AS no_aprobados,
            SUM(retirados)         AS retirados,
            ROUND(AVG(tasa_aprobacion)::numeric, 2) AS tasa_aprobacion_promedio,
            ROUND(AVG(tasa_desercion)::numeric, 2)  AS tasa_desercion_promedio
        FROM resumen_departamento
    """)
    row = db.execute(sql).fetchone()
    if not row:
        return {}
    return {
        "resumen": "RESUMEN NACIONAL 2024",
        "total_estudiantes": int(row[0] or 0),
        "aprobados": int(row[1] or 0),
        "no_aprobados": int(row[2] or 0),
        "retirados": int(row[3] or 0),
        "tasa_aprobacion_promedio": float(row[4] or 0),
        "tasa_desercion_promedio": float(row[5] or 0),
    }


def _query_departamentos(db: Session, orden_por: str = "tasa_aprobacion") -> list[dict]:
    columnas_validas = {
        "tasa_aprobacion", "tasa_desercion", "tasa_repitencia",
        "total_estudiantes", "departamento"
    }
    if orden_por not in columnas_validas:
        orden_por = "tasa_aprobacion"

    sql = text(f"""
        SELECT departamento, total_estudiantes, tasa_aprobacion,
               tasa_desercion, tasa_repitencia,
               porcentaje_publico, porcentaje_urbano, porcentaje_mujeres
        FROM resumen_departamento
        ORDER BY {orden_por} DESC NULLS LAST
        LIMIT 22
    """)
    rows = db.execute(sql).fetchall()
    return [
        {
            "departamento": r[0],
            "total_estudiantes": int(r[1] or 0),
            "tasa_aprobacion": float(r[2] or 0),
            "tasa_desercion": float(r[3] or 0),
            "tasa_repitencia": float(r[4] or 0),
            "porcentaje_publico": float(r[5] or 0),
            "porcentaje_urbano": float(r[6] or 0),
            "porcentaje_mujeres": float(r[7] or 0),
        }
        for r in rows
    ]


def _query_urbano_rural(db: Session) -> list[dict]:
    sql = text("""
        SELECT area, total_estudiantes, tasa_aprobacion,
               tasa_desercion, tasa_repitencia
        FROM resumen_urbano_rural
        ORDER BY area
    """)
    rows = db.execute(sql).fetchall()
    return [
        {
            "area": r[0],
            "total_estudiantes": int(r[1] or 0),
            "tasa_aprobacion": float(r[2] or 0),
            "tasa_desercion": float(r[3] or 0),
            "tasa_repitencia": float(r[4] or 0),
        }
        for r in rows
    ]


def _query_sector(db: Session) -> list[dict]:
    sql = text("""
        SELECT sector, total_estudiantes, tasa_aprobacion,
               tasa_desercion, tasa_repitencia
        FROM resumen_sector
        ORDER BY sector
    """)
    rows = db.execute(sql).fetchall()
    return [
        {
            "sector": r[0],
            "total_estudiantes": int(r[1] or 0),
            "tasa_aprobacion": float(r[2] or 0),
            "tasa_desercion": float(r[3] or 0),
            "tasa_repitencia": float(r[4] or 0),
        }
        for r in rows
    ]


def _query_sexo(db: Session) -> list[dict]:
    sql = text("""
        SELECT sexo, total_estudiantes, tasa_aprobacion,
               tasa_desercion, tasa_repitencia
        FROM resumen_sexo
        ORDER BY sexo
    """)
    rows = db.execute(sql).fetchall()
    return [
        {
            "sexo": r[0],
            "total_estudiantes": int(r[1] or 0),
            "tasa_aprobacion": float(r[2] or 0),
            "tasa_desercion": float(r[3] or 0),
            "tasa_repitencia": float(r[4] or 0),
        }
        for r in rows
    ]


def _query_top_desercion(db: Session, top_n: int = 5) -> list[dict]:
    sql = text(f"""
        SELECT departamento, tasa_desercion, total_estudiantes
        FROM resumen_departamento
        ORDER BY tasa_desercion DESC NULLS LAST
        LIMIT {top_n}
    """)
    rows = db.execute(sql).fetchall()
    return [
        {"departamento": r[0], "tasa_desercion": float(r[1] or 0), "total": int(r[2] or 0)}
        for r in rows
    ]


def _query_top_aprobacion(db: Session, top_n: int = 5) -> list[dict]:
    sql = text(f"""
        SELECT departamento, tasa_aprobacion, total_estudiantes
        FROM resumen_departamento
        ORDER BY tasa_aprobacion DESC NULLS LAST
        LIMIT {top_n}
    """)
    rows = db.execute(sql).fetchall()
    return [
        {"departamento": r[0], "tasa_aprobacion": float(r[1] or 0), "total": int(r[2] or 0)}
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Recuperación de contexto según intenciones
# ---------------------------------------------------------------------------

def recuperar_contexto(intenciones: list[str], db: Session) -> dict[str, Any]:
    """Ejecuta las queries necesarias y retorna el contexto como dict."""
    contexto: dict[str, Any] = {}

    if "nacional" in intenciones or not intenciones:
        contexto["resumen_nacional"] = _query_nacional(db)

    if "aprobacion" in intenciones:
        contexto["top_aprobacion"] = _query_top_aprobacion(db)
        if "resumen_nacional" not in contexto:
            contexto["resumen_nacional"] = _query_nacional(db)

    if "desercion" in intenciones:
        contexto["top_desercion"] = _query_top_desercion(db)
        contexto["resumen_departamentos"] = _query_departamentos(db, "tasa_desercion")

    if "repitencia" in intenciones:
        contexto["resumen_departamentos"] = _query_departamentos(db, "tasa_repitencia")

    if "urbano_rural" in intenciones:
        contexto["urbano_rural"] = _query_urbano_rural(db)

    if "sector" in intenciones:
        contexto["sector"] = _query_sector(db)

    if "sexo" in intenciones:
        contexto["sexo"] = _query_sexo(db)

    if "departamento" in intenciones:
        contexto["resumen_departamentos"] = _query_departamentos(db)

    return contexto


# ---------------------------------------------------------------------------
# Llamada a Claude con contexto RAG
# ---------------------------------------------------------------------------

def _formatear_contexto(contexto: dict[str, Any]) -> str:
    """Convierte el contexto a texto legible para el prompt."""
    import json
    return json.dumps(contexto, ensure_ascii=False, indent=2, default=str)


def llamar_claude(pregunta: str, contexto: dict[str, Any]) -> str:
    """Llama a Claude con contexto y retorna la respuesta de texto."""
    cliente = _get_claude_client()
    contexto_str = _formatear_contexto(contexto)

    user_message = f"""DATOS DEL INE GUATEMALA 2024:
{contexto_str}

PREGUNTA DEL USUARIO:
{pregunta}

Por favor responde basándote ÚNICAMENTE en los datos anteriores."""

    try:
        respuesta = cliente.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1024,
            temperature=0.3,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        return respuesta.content[0].text
    except anthropic.APIError as e:
        log.error("Error de Claude API: %s", e)
        raise


# ---------------------------------------------------------------------------
# Función principal del agente
# ---------------------------------------------------------------------------

def query_agente(pregunta: str, db: Session) -> dict[str, Any]:
    """
    Punto de entrada principal del agente IA.

    Returns:
        {
            "respuesta": str,
            "datos_usados": dict,
            "intenciones_detectadas": list[str],
            "confianza": float,       # 0-1 heurística
        }
    """
    log.info("Agente procesando: '%s'", pregunta[:80])

    # 1. Clasificar intención
    intenciones = clasificar_intencion(pregunta)
    log.info("Intenciones detectadas: %s", intenciones)

    # 2. Recuperar contexto de la BD
    contexto = recuperar_contexto(intenciones, db)

    if not contexto:
        return {
            "respuesta": "No tenemos información sobre eso en los datos disponibles.",
            "datos_usados": {},
            "intenciones_detectadas": intenciones,
            "confianza": 0.0,
        }

    # 3. Llamar a Claude
    try:
        respuesta_texto = llamar_claude(pregunta, contexto)
    except Exception as e:
        log.error("Error al llamar Claude: %s", e)
        # Fallback: respuesta directa de datos sin IA
        respuesta_texto = _respuesta_fallback(contexto, intenciones)

    # 4. Heurística de confianza (basada en si hay datos)
    confianza = 0.95 if contexto else 0.0

    return {
        "respuesta": respuesta_texto,
        "datos_usados": contexto,
        "intenciones_detectadas": intenciones,
        "confianza": confianza,
    }


def _respuesta_fallback(contexto: dict[str, Any], intenciones: list[str]) -> str:
    """Genera una respuesta básica cuando Claude no está disponible."""
    partes = []

    if "resumen_nacional" in contexto:
        r = contexto["resumen_nacional"]
        partes.append(
            f"Resumen nacional 2024: {r.get('total_estudiantes', 'N/D'):,} estudiantes. "
            f"Tasa de aprobación promedio: {r.get('tasa_aprobacion_promedio', 'N/D')}%. "
            f"Tasa de deserción: {r.get('tasa_desercion_promedio', 'N/D')}%."
        )

    if "urbano_rural" in contexto:
        for area in contexto["urbano_rural"]:
            partes.append(
                f"Área {area['area']}: {area['total_estudiantes']:,} estudiantes, "
                f"aprobación {area['tasa_aprobacion']}%."
            )

    if "sector" in contexto:
        for s in contexto["sector"]:
            partes.append(
                f"Sector {s['sector']}: {s['total_estudiantes']:,} estudiantes, "
                f"aprobación {s['tasa_aprobacion']}%."
            )

    if not partes:
        return "No tenemos información sobre eso en los datos disponibles."

    return " ".join(partes) + " (Nota: respuesta generada directamente de datos, sin IA)."
