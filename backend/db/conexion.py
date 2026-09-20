import os
import sqlite3
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "educacion.db"

def get_connection():
    """
    Retorna una conexion activa a la base de datos SQLite educacion.db.
    Habilita soporte para diccionarios (row_factory).
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query: str, params: tuple = ()):
    """
    Ejecuta una consulta SQL y devuelve los resultados como lista de diccionarios.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def execute_write(query: str, params: tuple = ()):
    """
    Ejecuta un comando de escritura (INSERT, UPDATE, DELETE).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

if __name__ == "__main__":
    print(f"Ruta de base de datos configurada: {DB_PATH}")
    with get_connection() as conn:
        print("Conexion SQLite exitosa.")
