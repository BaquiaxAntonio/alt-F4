"""
Modelos SQLAlchemy para el esquema de base de datos.
Tablas:
  - inscripciones       → dataset principal decodificado (~4.3M registros)
  - resumen_departamento → agregaciones por departamento (22 filas)
  - resumen_urbano_rural → agregaciones urbano / rural
  - resumen_sector       → agregaciones público / privado
  - resumen_sexo         → agregaciones hombre / mujer
"""
from __future__ import annotations

from decimal import Decimal
from sqlalchemy import (
    Column, Integer, String, Numeric, BigInteger, Index, text
)
from backend.db.conexion import Base


class Inscripcion(Base):
    """Registro individual de inscripción (decodificado)."""
    __tablename__ = "inscripciones"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Identificadores geográficos / administrativos
    departamento = Column(String(100), nullable=False, index=True)
    municipio = Column(String(100), nullable=True, index=True)
    sector = Column(String(50), nullable=True)     # Público / Privado
    area = Column(String(50), nullable=True)        # Urbana / Rural
    zona = Column(String(50), nullable=True)

    # Clasificación educativa
    nivel = Column(String(100), nullable=True)
    grado = Column(String(50), nullable=True)
    pueblo = Column(String(100), nullable=True)     # Pueblo de pertenencia

    # Demografía
    sexo = Column(String(20), nullable=True)        # Hombre / Mujer

    # Resultados
    resultado = Column(String(50), nullable=True)   # Promovido / No promovido / Retirado

    # Cantidades (agregadas por fila en el dataset original)
    total_estudiantes = Column(Integer, nullable=False, default=0)
    aprobados = Column(Integer, nullable=False, default=0)
    no_aprobados = Column(Integer, nullable=False, default=0)
    retirados = Column(Integer, nullable=False, default=0)

    # Métricas derivadas
    tasa_aprobacion = Column(Numeric(6, 2), nullable=True)
    tasa_desercion = Column(Numeric(6, 2), nullable=True)
    tasa_repitencia = Column(Numeric(6, 2), nullable=True)

    # Año del registro
    anio = Column(Integer, nullable=False, default=2024)

    __table_args__ = (
        Index("idx_inscripciones_depto_sector", "departamento", "sector"),
        Index("idx_inscripciones_area", "area"),
        Index("idx_inscripciones_resultado", "resultado"),
    )


class ResumenDepartamento(Base):
    """Agregación a nivel departamento (22 filas)."""
    __tablename__ = "resumen_departamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    departamento = Column(String(100), nullable=False, unique=True, index=True)
    codigo_departamento = Column(Integer, nullable=True)

    total_estudiantes = Column(BigInteger, nullable=False, default=0)
    aprobados = Column(BigInteger, nullable=False, default=0)
    no_aprobados = Column(BigInteger, nullable=False, default=0)
    retirados = Column(BigInteger, nullable=False, default=0)

    tasa_aprobacion = Column(Numeric(6, 2), nullable=True)   # 0-100
    tasa_desercion = Column(Numeric(6, 2), nullable=True)
    tasa_repitencia = Column(Numeric(6, 2), nullable=True)

    # Desagregaciones rápidas
    porcentaje_publico = Column(Numeric(6, 2), nullable=True)
    porcentaje_urbano = Column(Numeric(6, 2), nullable=True)
    porcentaje_mujeres = Column(Numeric(6, 2), nullable=True)

    anio = Column(Integer, nullable=False, default=2024)


class ResumenUrbanoRural(Base):
    """Agregación urbano vs rural (2 filas)."""
    __tablename__ = "resumen_urbano_rural"

    id = Column(Integer, primary_key=True, autoincrement=True)
    area = Column(String(50), nullable=False, unique=True)   # Urbana | Rural

    total_estudiantes = Column(BigInteger, nullable=False, default=0)
    aprobados = Column(BigInteger, nullable=False, default=0)
    no_aprobados = Column(BigInteger, nullable=False, default=0)
    retirados = Column(BigInteger, nullable=False, default=0)

    tasa_aprobacion = Column(Numeric(6, 2), nullable=True)
    tasa_desercion = Column(Numeric(6, 2), nullable=True)
    tasa_repitencia = Column(Numeric(6, 2), nullable=True)

    anio = Column(Integer, nullable=False, default=2024)


class ResumenSector(Base):
    """Agregación público vs privado (2 filas)."""
    __tablename__ = "resumen_sector"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sector = Column(String(50), nullable=False, unique=True)  # Público | Privado

    total_estudiantes = Column(BigInteger, nullable=False, default=0)
    aprobados = Column(BigInteger, nullable=False, default=0)
    no_aprobados = Column(BigInteger, nullable=False, default=0)
    retirados = Column(BigInteger, nullable=False, default=0)

    tasa_aprobacion = Column(Numeric(6, 2), nullable=True)
    tasa_desercion = Column(Numeric(6, 2), nullable=True)
    tasa_repitencia = Column(Numeric(6, 2), nullable=True)

    anio = Column(Integer, nullable=False, default=2024)


class ResumenSexo(Base):
    """Agregación por sexo (Hombre / Mujer)."""
    __tablename__ = "resumen_sexo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sexo = Column(String(20), nullable=False, unique=True)

    total_estudiantes = Column(BigInteger, nullable=False, default=0)
    aprobados = Column(BigInteger, nullable=False, default=0)
    no_aprobados = Column(BigInteger, nullable=False, default=0)
    retirados = Column(BigInteger, nullable=False, default=0)

    tasa_aprobacion = Column(Numeric(6, 2), nullable=True)
    tasa_desercion = Column(Numeric(6, 2), nullable=True)
    tasa_repitencia = Column(Numeric(6, 2), nullable=True)

    anio = Column(Integer, nullable=False, default=2024)
