"""
Aplicación principal FastAPI - Hackathon AI Builders GT 2026
Análisis de Datos Educativos de Guatemala (INE 2024)

Equipo: alt-F4
"""
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan: inicializa la BD al arrancar
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Iniciando backend de Educación Guatemala...")
    try:
        from backend.db.conexion import engine
        from backend.db.models import Base
        Base.metadata.create_all(bind=engine)
        log.info("✅ Tablas verificadas/creadas en PostgreSQL.")
    except Exception as e:
        log.warning("⚠️  No se pudo conectar a PostgreSQL al iniciar: %s", e)
        log.warning("   El servidor arranca igualmente. Verifica DATABASE_URL en .env")
    yield
    log.info("Backend detenido.")


# ---------------------------------------------------------------------------
# Aplicación FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(
    title="API - Análisis Educativo Guatemala",
    description=(
        "API REST para análisis de 4.3 millones de registros educativos del INE Guatemala (2024). "
        "Incluye endpoints de datos agregados y un agente IA (Claude) con patrón RAG."
    ),
    version="1.0.0",
    contact={
        "name": "Equipo alt-F4",
        "url": "https://github.com/BaquiaxAntonio/alt-F4",
    },
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — permitir frontend (React en Vite)
# ---------------------------------------------------------------------------

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Registrar routers
# ---------------------------------------------------------------------------

from backend.api.endpoints import router as api_router  # noqa: E402

app.include_router(api_router)


# ---------------------------------------------------------------------------
# Ruta raíz informativa
# ---------------------------------------------------------------------------

@app.get("/", tags=["info"])
def root():
    return {
        "proyecto": "Análisis Educativo Guatemala - Hackathon AI Builders GT 2026",
        "equipo": "alt-F4",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints_principales": [
            "GET /api/resumen",
            "GET /api/departamentos",
            "GET /api/departamento/{nombre}",
            "GET /api/comparativas?tipo=urbano_rural",
            "POST /api/buscar",
            "GET /api/health",
        ],
    }


# ---------------------------------------------------------------------------
# Entry point para desarrollo directo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
