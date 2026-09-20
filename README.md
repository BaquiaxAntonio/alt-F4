# Plataforma de Análisis Educativo Guatemala - Hackathon AI Builders GT

Plataforma interactiva y conversacional con IA para la exploración, visualización y análisis de datos educativos de Guatemala (Ministerio de Educación / INE 2024).

---

## Estructura del Módulo de Datos (Data Engineer)

```
alt-F4/
├── data/
│   ├── raw/                           # Directorio para archivos XLSX crudos del INE
│   ├── processed/                     # Salidas limpias y JSONs de consumo rápido
│   │   ├── resumen_nacional.json      # Métricas consolidadas del país
│   │   ├── resumen_departamentos.json # Datos agregados de los 22 departamentos
│   │   └── comparativas.json          # Datos urbano/rural, sectores y género
│   └── diccionario_variables.json     # Mapeo oficial de códigos INE a etiquetas
├── backend/
│   ├── db/
│   │   └── conexion.py                # Conexión portable SQLite / Helper SQL
│   └── ingesta/
│       ├── generar_bd_inicial.py      # Generador exprés de BD y JSONs de mock
│       ├── procesar_datos.py          # Pipeline ETL con Pandas para XLSX/CSV crudos
│       └── validar_datos.py           # Auditoría matemática de calidad y consistencia
├── educacion.db                       # Base de datos SQLite funcional y precomputada
└── VALIDACION_INGESTA.md              # Reporte de certificación técnica de datos
```

---

## 🚀 Guía Rápida de Uso para el Equipo

### 1. Para Persona 2 (Backend Developer)
- **Base de Datos SQLite:** Conéctate directamente a `educacion.db` usando `backend/db/conexion.py` o tu ORM favorito (SQLAlchemy / Tortoise).
- **Tablas disponibles:**
  - `resumen_nacional`: métricas globales (estudiantes, aprobados, retirados, tasas).
  - `resumen_departamento`: 22 departamentos con desglose de tasas y brecha urbana/rural.
  - `resumen_area`: comparación Urbana vs Rural.
  - `resumen_sector`: Oficial (Público), Privado, Cooperativa, Municipal.
  - `resumen_sexo`: Hombre vs Mujer.
  - `inscripciones_muestra`: 100 registros representativos para pruebas del Agente IA (`/api/buscar`).
- **Mocks JSON para desarrollo inmediato:**
  - `data/processed/resumen_nacional.json` (para `/api/resumen`)
  - `data/processed/resumen_departamentos.json` (para `/api/departamentos`)
  - `data/processed/comparativas.json` (para `/api/comparativas`)

### 2. Para Persona 3 y 4 (Frontend Developers)
Pueden consumir los JSONs de `data/processed/` directamente o mediante la API de FastAPI para diseñar los dashboards, gráficas (Recharts/Plotly) y el chat widget.

### 3. Comandos de Mantenimiento de Datos

- **Regenerar base de datos y JSONs iniciales:**
  ```bash
  python backend/ingesta/generar_bd_inicial.py
  ```

- **Ejecutar auditoría de consistencia matemática:**
  ```bash
  python backend/ingesta/validar_datos.py
  ```

- **Procesar nuevos archivos XLSX/CSV ubicados en `data/raw/`:**
  ```bash
  python backend/ingesta/procesar_datos.py
  ```

---

## Certificación de Calidad
Consulta [VALIDACION_INGESTA.md](VALIDACION_INGESTA.md) para ver el reporte de calidad técnica con los 10 checks aprobados al 100%.
