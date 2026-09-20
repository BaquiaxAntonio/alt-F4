# Análisis de Datos Educativos de Guatemala
## Hackathon AI Builders GT 2026 — Equipo alt-F4

Plataforma conversacional que transforma 4.3 millones de registros del INE en análisis interactivo con IA.

---

## ¿Qué hace esta solución?

1. **Ingesta** → Lee 22 archivos XLSX del INE, decodifica variables, calcula métricas y carga en PostgreSQL
2. **API REST** → FastAPI con 5 endpoints principales + agente IA (Claude con RAG)
3. **Frontend** → React + Recharts con dashboard, filtros y chat

---

## Requisitos

- Docker y Docker Compose
- (Opcional para desarrollo local) Python 3.12+, Node.js 22+

---

## Instalación y Ejecución

### Con Docker (recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/BaquiaxAntonio/alt-F4.git
cd alt-F4

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu ANTHROPIC_API_KEY

# 3. Colocar los archivos XLSX del INE en /data/raw/
#    Descarga desde: https://datos.ine.gob.gt/dataset/educacion-formal-2024

# 4. Levantar servicios (DB + Backend + Frontend)
docker-compose up -d

# 5. Ejecutar ingesta (primera vez o cuando cambien los datos)
docker-compose --profile ingesta up ingesta

# 6. Verificar que funciona
curl http://localhost:8000/api/health
```

### Desarrollo local (sin Docker)

```bash
# ─── Backend ─────────────────────────────────────────
cd alt-F4
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# Necesitas PostgreSQL corriendo localmente
# Configura DATABASE_URL en .env

# Arrancar backend
uvicorn backend.main:app --reload

# ─── Ingesta ─────────────────────────────────────────
python -m backend.ingesta.script_procesar_datos

# ─── Frontend ─────────────────────────────────────────
npm install
npm run dev
```

---

## Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Estado del backend |
| GET | `/api/resumen` | KPIs nacionales |
| GET | `/api/departamentos` | 22 departamentos con métricas |
| GET | `/api/departamento/{nombre}` | Detalle de un departamento |
| GET | `/api/comparativas?tipo=urbano_rural` | Comparativas temáticas |
| POST | `/api/buscar` | Agente IA (RAG con Claude) |

Documentación interactiva: http://localhost:8000/docs

---

## Estructura del Proyecto

```
alt-f4/
├── backend/
│   ├── main.py              # App FastAPI
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── api/
│   │   ├── endpoints.py     # Rutas REST
│   │   └── agente_ia.py     # Agente Claude con RAG
│   ├── db/
│   │   ├── models.py        # Esquema SQLAlchemy
│   │   └── conexion.py      # Conexión PostgreSQL
│   └── ingesta/
│       └── script_procesar_datos.py  # ETL datos INE
├── data/
│   ├── raw/                 # Archivos XLSX (no en Git)
│   ├── processed/           # CSVs intermedios (no en Git)
│   └── diccionario_variables.json  # Mapeo de códigos
├── src/                     # Frontend React
├── docker-compose.yml
├── .env.example
└── GUIA_DESARROLLO_HACKATHON.md
```

---

## Configuración de Variables de Entorno

```env
DATABASE_URL=postgresql://hackathon:hackathon123@localhost:5432/educacion_gt
ANTHROPIC_API_KEY=sk-ant-...   # Obligatorio para el agente IA
VITE_API_URL=http://localhost:8000
```

---

## Datos

- **Fuente:** INE Guatemala — Educación Formal 2024
- **URL:** https://datos.ine.gob.gt/dataset/educacion-formal-2024
- **Formato:** 22 archivos XLSX (uno por departamento)
- **Volumen:** ~4.3 millones de registros

Los archivos XLSX **no están en el repositorio** por su tamaño. Descárgalos del enlace oficial y colócalos en `/data/raw/`.

---

## Equipo

**alt-F4** — Hackathon AI Builders GT 2026
