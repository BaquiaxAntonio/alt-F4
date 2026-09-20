# Análisis de Datos Educativos de Guatemala
## Hackathon AI Builders GT 2026 — Equipo alt-F4

Plataforma interactiva y conversacional con IA para la exploración, visualización y análisis de datos educativos de Guatemala (Ministerio de Educación / INE 2024), transformando más de 4.3 millones de registros en respuestas y visualizaciones accionables.

---

## ¿Qué hace esta solución?

1. **Ingesta y Datos (Data Engineer)** → Decodificación de variables del INE con diccionario oficial, generación de agregaciones demográficas/geográficas, validación matemática de consistencia y soporte para SQLite local o PostgreSQL en producción.
2. **API REST (Backend)** → Servidor FastAPI con endpoints optimizados para KPIs nacionales, departamentales, comparativas y un endpoint inteligente con IA (`/api/buscar`) usando Claude + RAG.
3. **Frontend Interactivo** → Dashboard responsivo en React + Recharts con filtros en tiempo real, mapas comparativos y widget conversacional.

---

## Requisitos

- Python 3.12+
- Node.js 20+
- (Opcional) Docker y Docker Compose

---

## Instalación y Ejecución

### Opción A: Con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/BaquiaxAntonio/alt-F4.git
cd alt-F4

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu ANTHROPIC_API_KEY

# 3. Colocar los archivos XLSX del INE en /data/raw/ (opcional para reprocesar)
#    Descarga desde: https://datos.ine.gob.gt/dataset/educacion-formal-2024

# 4. Levantar servicios (DB + Backend + Frontend)
docker-compose up -d

# 5. Ejecutar ingesta completa (primera vez o cuando cambien los datos)
docker-compose --profile ingesta up ingesta

# 6. Verificar que funciona
curl http://localhost:8000/api/health
```

### Opción B: Desarrollo Local Rápido (Sin Docker)

```bash
# ─── Backend ─────────────────────────────────────────
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

pip install -r backend/requirements.txt

# Generar o verificar la base de datos local (SQLite) y datos mock:
python backend/ingesta/generar_bd_inicial.py

# Arrancar backend
uvicorn backend.main:app --reload

# ─── Frontend ─────────────────────────────────────────
npm install
npm run dev
```

---

## Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Estado del backend |
| GET | `/api/resumen` | KPIs nacionales de aprobación, deserción y repitencia |
| GET | `/api/departamentos` | 22 departamentos con métricas detalladas |
| GET | `/api/departamento/{nombre}` | Detalle de un departamento específico |
| GET | `/api/comparativas?tipo=urbano_rural` | Comparativas urbano/rural, sector y género |
| POST | `/api/buscar` | Agente IA (RAG con Claude) |

Documentación interactiva Swagger: http://localhost:8000/docs

---

## Estructura del Proyecto

```
alt-f4/
├── backend/
│   ├── main.py                     # App FastAPI
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── api/
│   │   ├── endpoints.py            # Rutas REST
│   │   └── agente_ia.py            # Agente Claude con RAG
│   ├── db/
│   │   ├── models.py               # Esquema SQLAlchemy
│   │   └── conexion.py             # Conexión dual PostgreSQL / SQLite
│   └── ingesta/
│       ├── generar_bd_inicial.py   # Setup rápido de BD y JSONs de mock
│       ├── script_procesar_datos.py# ETL datos INE (PostgreSQL)
│       ├── procesar_datos.py       # Pipeline ETL modular Pandas
│       └── validar_datos.py        # Auditoría matemática de calidad
├── data/
│   ├── raw/                        # Archivos XLSX crudos (no versionados)
│   ├── processed/                  # JSONs de consulta rápida para frontend/backend
│   │   ├── resumen_nacional.json
│   │   ├── resumen_departamentos.json
│   │   └── comparativas.json
│   └── diccionario_variables.json  # Mapeo oficial de códigos INE
├── src/                            # Frontend React + Vite
├── educacion.db                    # Base de datos SQLite local precomputada
├── VALIDACION_INGESTA.md           # Certificación técnica de datos (10/10 checks)
├── docker-compose.yml
├── .env.example
└── GUIA_DESARROLLO_HACKATHON.md
```

---

## Validación y Certificación de Calidad

Para verificar la consistencia matemática y estadísticas de los datos:
```bash
python backend/ingesta/validar_datos.py
```
Consulta los resultados detallados en [VALIDACION_INGESTA.md](VALIDACION_INGESTA.md).

---

## Equipo

**alt-F4** — Hackathon AI Builders GT 2026
