"""
Módulo de conexión a Base de Datos (PostgreSQL vía SQLAlchemy / SQLite local).
"""
import os
import sqlite3
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "educacion.db"

# URL de conexión (PostgreSQL por defecto en Docker/producción, SQLite como fallback portable)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DB_PATH}" if not os.getenv("USE_POSTGRES") else "postgresql://hackathon:hackathon123@localhost:5432/educacion_gt"
)


class Base(DeclarativeBase):
    pass


# Configurar engine con argumentos según motor
is_sqlite = DATABASE_URL.startswith("sqlite")
engine_kwargs = {"connect_args": {"check_same_thread": False}} if is_sqlite else {
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency para obtener sesión de BD en FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Crea todas las tablas definidas en los modelos."""
    from backend.db.models import Base  # noqa: F401
    Base.metadata.create_all(bind=engine)


# ─── Helpers de conexión directa SQLite para ingesta rápida ───
def get_connection():
    """Retorna conexión directa SQLite para scripts de ingesta y validación rápida."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query: str, params: tuple = ()):
    """Ejecuta una consulta SQL y devuelve los resultados como lista de diccionarios."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def execute_write(query: str, params: tuple = ()):
    """Ejecuta un comando de escritura (INSERT, UPDATE, DELETE)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


if __name__ == "__main__":
    print(f"DATABASE_URL: {DATABASE_URL}")
    print(f"Ruta SQLite local: {DB_PATH}")
    with get_connection() as conn:
        print("Conexión SQLite exitosa.")
