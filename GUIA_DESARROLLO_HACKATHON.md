# Guía de Desarrollo Hackathon AI Builders GT
## Análisis de Datos Educativos con IA

**Objetivo:** Transformar 4.3 millones de registros opacos en una solución web interactiva que traduce, explica y responde preguntas sobre educación en Guatemala.

---

## ÍNDICE
1. Análisis del Desafío
2. Propuesta de Solución
3. Stack Tecnológico Recomendado
4. Arquitectura del Proyecto
5. Componentes Principales
6. Plan de Desarrollo Paso a Paso
7. Validaciones en Cada Etapa
8. Estrategia de Presentación (Pitch)

---

## 1. ANÁLISIS DEL DESAFÍO

### El Problema Real

**Barreras de interpretación identificadas:**

| Barrera | Impacto | Solución |
|---------|--------|---------|
| **Datos codificados** | "1" no significa nada sin diccionario | Decodificación automática con mapping |
| **Volumen abrumador** | 4.3M filas = imposible en hoja de cálculo | Agregación inteligente + estadísticas |
| **Falta de indicadores** | No hay columnas de "aprobación" o "deserción" | Ingesta calcula métricas derivadas |
| **No hay contexto** | Números aislados no comunican | Análisis escrito + comparativas + narrativa |

### Usuarios Objetivo

- **Autoridades municipales** → Necesitan decisiones sobre presupuesto educativo
- **Periodistas de datos** → Buscan historias y evidencia
- **Docentes y directores** → Quieren entender su comunidad educativa
- **Investigadores** → Requieren cifras confiables y comparables

### Insights Clave

El dataset permite responder preguntas reales:
- ¿En qué departamento se aprueba menos primaria?
- ¿Dónde es mayor la brecha entre urbano y rural?
- ¿Cómo varía la aprobación por sexo y pueblo de pertenencia?

**Oportunidad:** No es solo visualización, es **traducir datos complejos en narrativa inteligente**.

---

## 2. PROPUESTA DE SOLUCIÓN

### Concepto: "Plataforma Conversacional de Análisis Educativo"

No es solo un dashboard. Es una **experiencia de tres capas**:

```
CAPA 1: VISUALIZACIÓN NARRATIVA
└─ Dashboard con gráficas, contexto y análisis escrito
└─ Cada visualización tiene una "historia" acompañante
└─ Indicadores clave explicados en lenguaje natural

CAPA 2: EXPLORACIÓN INTERACTIVA
└─ Filtros inteligentes (departamento, sector, zona, resultado)
└─ Vistas que se actualizan en tiempo real
└─ Comparativas side-by-side

CAPA 3: CONSULTA CON IA
└─ Chatbot que responde preguntas sobre los datos
└─ "¿Qué departamento tiene más deserción?"
└─ "¿Cómo es la aprobación en el área rural vs urbana?"
└─ Genera respuestas basadas en datos reales, no alucinaciones
```

### Por qué esto supera un dashboard tradicional

1. **Narrativa + Datos:** Las gráficas no hablan solas; cada una tiene un párrafo de análisis
2. **Interactividad:** El usuario no solo consume, explora y pregunta
3. **IA Responsable:** El agente reconoce límites y cita fuentes (datos concretos)
4. **Accesibilidad:** Diseñado para personas sin formación estadística

---

## 3. STACK TECNOLÓGICO RECOMENDADO

### Frontend (Interfaz Web)

**Framework:** React o Next.js
- **Por qué:** Componentes reutilizables, estado reactivo, excelente para dashboards
- **Ventaja adicional:** Fácil integración con APIs de IA
- **Alternativa ligera:** Vue.js si prefieres curva menos pronunciada

**Visualización de datos:** Plotly.js o Recharts
- **Por qué:** Gráficas interactivas, accesibles, sin complejidad
- **Caso de uso:** Líneas, barras, mapas geográficos de departamentos

**UI/Componentes:** Shadcn/ui o Material-UI
- **Por qué:** Temas claros, componentes profesionales, accesibilidad

**Hospedaje:** Vercel (Next.js) o Netlify (React)
- **Por qué:** Despliegue automático desde GitHub, HTTPS, CDN global

---

### Backend (Ingesta y API)

**Servidor:** Python con FastAPI
- **Por qué:** Fácil procesamiento de datos, buenas librerías de IA, rápido de iterar
- **Alternativa:** Node.js + Express (si todo el equipo es JS)

**Procesamiento de datos:** Pandas + NumPy
- **Por qué:** Estándar para ingesta y transformación
- **Pipeline:** 
  - Lectura de archivos XLSX
  - Decodificación con diccionario de variables
  - Cálculo de métricas (aprobación, deserción, repitencia)
  - Agregación por dimensiones (departamento, sector, zona, etc.)

**Base de datos:** PostgreSQL
- **Por qué:** Estructurada, relacional, excelente para agregaciones complejas
- **Alternativa:** SQLite si lo quieres local (más simple, menos escalable)

**API REST:** FastAPI con endpoints para:
- `/api/resumen` → Indicadores generales
- `/api/departamentos` → Datos por departamento
- `/api/comparativas` → Urbano vs rural, público vs privado, etc.
- `/api/buscar` → Endpoint que acepta preguntas (para el agente)

---

### IA y Procesamiento de Lenguaje Natural

**Modelo LLM:** Claude API (Anthropic) o GPT-4 (OpenAI)
- **Por qué Claude:** Excelente para análisis responsable, reconoce límites, evita alucinaciones
- **Configuración:** Temperature baja (0.3-0.5) para respuestas precisas
- **Presupuesto:** Consultar costos; considera cache o batch processing

**RAG (Retrieval-Augmented Generation):**
- El agente NO memoriza 4.3M registros
- En su lugar: pregunta → búsqueda en base de datos → contexto → respuesta LLM
- Garantiza que responde solo con datos reales del dataset

**Embeddings (opcional):** Para búsqueda semántica
- Si quieres que el agente encuentre análisis similares

**Orquestación:** LangChain o simple con llamadas a API
- Maneja el flujo: pregunta → búsqueda BD → prompt → LLM → respuesta

---

### Infraestructura y DevOps

**Contenedores:** Docker
- **Por qué:** Reproducibilidad garantizada (critério de evaluación)
- **Estructura:** Dockerfile para backend, para ingesta, docker-compose orquesta todo

**Control de versiones:** GitHub
- **Rama main:** código estable
- **Rama develop:** cambios en progreso
- **.gitignore:** credenciales de IA, datos grandes, dependencias

**Almacenamiento de datos:** 
- Datos procesados en BD (PostgreSQL)
- Datos crudos en carpeta `/data/raw` (no versionados en Git)
- Diccionario de variables en repositorio (pequeño y crucial)

---

## 4. ARQUITECTURA DEL PROYECTO

### Diagrama Conceptual

```
INGESTA (Batch)
  ├─ Script Python que lee XLSX
  ├─ Decodifica con diccionario_variables.json
  ├─ Calcula métricas
  └─ Carga en PostgreSQL
         ↓
BACKEND (API REST)
  ├─ FastAPI server
  ├─ Endpoints de consultas SQL → JSON
  ├─ Validación de datos
  └─ Integración con Claude API
         ↓
FRONTEND (Web Interactive)
  ├─ React/Next.js
  ├─ Dashboards visuales
  ├─ Filtros interactivos
  └─ Chat widget para consultas
         ↓
USUARIO
  └─ Ve gráficas, lee análisis, hace preguntas
```

### Estructura de Carpetas

```
proyecto-hackathon/
│
├─ README.md (instrucciones de reproducibilidad)
├─ ARQUITECTURA.md (decisiones técnicas)
├─ .env.example (variables de entorno sin secretos)
├─ docker-compose.yml
│
├─ /data
│   ├─ /raw (archivos XLSX sin procesar)
│   ├─ /processed (CSVs/JSONs intermedios)
│   └─ diccionario_variables.json (CRÍTICO)
│
├─ /backend
│   ├─ main.py (app FastAPI)
│   ├─ requirements.txt
│   ├─ Dockerfile
│   ├─ /ingesta
│   │   └─ script_procesar_datos.py
│   ├─ /api
│   │   ├─ endpoints.py
│   │   └─ agente_ia.py
│   └─ /db
│       ├─ models.py (esquema BD)
│       └─ conexion.py
│
├─ /frontend
│   ├─ package.json
│   ├─ Dockerfile
│   ├─ /src
│   │   ├─ App.jsx
│   │   ├─ /components
│   │   │   ├─ Dashboard.jsx
│   │   │   ├─ Filtros.jsx
│   │   │   └─ ChatAgent.jsx
│   │   ├─ /pages
│   │   ├─ /utils (llamadas a API)
│   │   └─ /styles
│   └─ .env.local (URL del backend)
│
└─ /docs
    ├─ VIDEO_1_arquitectura.md (guion)
    ├─ VIDEO_2_funcionamiento.md (guion)
    └─ PITCH_notas.md (5 min de presentación)
```

---

## 5. COMPONENTES PRINCIPALES

### 5.1 INGESTA DE DATOS

**Responsabilidad:** Leer crudos, decodificar, calcular, persistir.

**Entrada:** 22 archivos XLSX (uno por departamento) + 1 diccionario

**Proceso:**
1. **Lectura:**
   - Pandas lee cada XLSX
   - Valida esquema (15 columnas esperadas)

2. **Decodificación:**
   - Carga diccionario_variables.json
   - Mapea códigos numéricos a etiquetas legibles
   - Ej: `1` → "Público", `5` → "No promovido"

3. **Cálculo de métricas derivadas:**
   - **Tasa de aprobación** = (aprobados / total) × 100
   - **Tasa de deserción** = (retirados / total) × 100
   - **Tasa de repitencia** = (repiten / total) × 100
   - Por cada dimensión: departamento, sector, zona, sexo, pueblo

4. **Validación:**
   - Verifica que cifras sean coherentes
   - Detecta anomalías (aprobación > 100%, etc.)
   - Log de advertencias

5. **Persistencia:**
   - Carga en PostgreSQL
   - Tabla central: `inscripciones` (4.3M registros decodificados)
   - Tablas agregadas: `resumen_departamento`, `resumen_sector`, etc. (para queries rápidas)

**Validación en esta etapa:**
- ✅ Todos los registros se cargaron
- ✅ Ceros ficticios (`9` = Ignorado) se tratan correctamente
- ✅ Las sumas de totales cierran con el dataset original
- ✅ Las métricas están entre 0 y 100

---

### 5.2 BACKEND API

**Responsabilidad:** Servir datos e integrar IA.

**Endpoints principales:**

| Endpoint | Método | Propósito | Ej. respuesta |
|----------|--------|----------|--------------|
| `/api/resumen` | GET | Indicadores nacionales | `{ total_estudiantes: 4.3M, aprobacion: 87%, ... }` |
| `/api/departamentos` | GET | Lista con métricas | `[ { nombre: "Guatemala", aprobacion: 88%, ... } ]` |
| `/api/departamento/:id` | GET | Detalle de 1 depto | Desagregado por sector, zona, sexo |
| `/api/comparativas?tipo=urbano_rural` | GET | Urbano vs rural | `{ urbano: {...}, rural: {...} }` |
| `/api/buscar?q=pregunta` | POST | Agente de IA | `{ respuesta: "...", datos_usados: [...], confianza: 0.95 }` |

**Lógica del endpoint `/api/buscar`:**

```
1. Recibe: "¿En qué departamento hay más deserción?"
2. Clasifica: pregunta es sobre "deserción"
3. Ejecuta SQL: SELECT departamento, tasa_desercion FROM resumen_depto ORDER BY tasa_desercion DESC
4. Obtiene resultado: [{ depto: "Huehuetenango", tasa: 12.5% }, ...]
5. Construye prompt para Claude con:
   - Pregunta original
   - Datos obtenidos
   - Instrucción: "Responde en lenguaje natural. Si no hay datos, dilo."
6. Llama Claude API
7. Devuelve respuesta + datos_usados (transparencia)
```

**Validación en esta etapa:**
- ✅ Todos los endpoints responden en < 2 segundos
- ✅ Las cifras en respuestas coinciden con base de datos
- ✅ El agente responde solo preguntas que los datos pueden responder
- ✅ No hay SQL injection ni acceso a datos sensibles (no hay IDs de estudiantes)

---

### 5.3 FRONTEND INTERACTIVO

**Responsabilidad:** Visualizar, contextualizar, permitir exploración.

**Secciones principales:**

#### A. Vista "Inicio" (Resumen Ejecutivo)
- **Componente:** Cards con KPIs nacionales
  - Total de estudiantes
  - Tasa de aprobación nacional
  - Comparativa urbano/rural
  - Distribución por sector (público/privado)
- **Análisis acompañante:** 
  - "En 2024 se inscribieron 4.3M estudiantes. La aprobación fue del 87%, pero varía entre departamentos..."
  - Párrafo que responde por qué estos números importan

#### B. Vista "Departamentos" (Exploración)
- **Tabla interactiva:** Todos los departamentos con indicadores
  - Ordenable por columnas
  - Clickeable para detalle
- **Mapa de Guatemala:** Visualización choropleth (colores según aprobación/deserción)
- **Gráfico comparativo:** Top 5 mejores/peores por indicador seleccionado
- **Análisis:** "Huehuetenango tiene la deserción más alta (12.5%). Esto contrasta con..."

#### C. Vista "Análisis Temático" (Temas pregrabados)
- Tabs para diferentes análisis:
  - **Brecha urbano-rural**
  - **Disparidades por sexo**
  - **Público vs privado**
  - **Por pueblo de pertenencia** (si los datos lo permiten)
- Cada tab tiene:
  - Gráficas lado a lado
  - Análisis escrito
  - Conclusiones

#### D. Vista "Chat" (Agente IA)
- **Widget conversacional** en la esquina inferior derecha
- **Historial de mensajes**
- **Ejemplos de preguntas sugeridas:**
  - "¿Cuál es la tasa de aprobación en el área rural?"
  - "¿Qué departamento tiene mayor deserción?"
  - "¿Cómo es la brecha entre hombres y mujeres?"
- **Respuestas del agente:**
  - Texto en lenguaje natural
  - Badge con "Basado en datos" o "No tenemos esos datos"
  - Opción de ver datos crudos que usó

**Validación en esta etapa:**
- ✅ Las gráficas coinciden con datos del backend
- ✅ Los análisis escritos son correctos y no engañan
- ✅ El chat responde en < 5 segundos
- ✅ La interfaz es usable en móvil (responsive)
- ✅ Contraste y legibilidad cumplen estándares WCAG

---

## 6. PLAN DE DESARROLLO PASO A PASO

### Semana 1: Fundamentos

#### Día 1-2: Preparación y Setup
**Tareas:**
- [ ] Clonar/iniciar repositorio en GitHub
- [ ] Crear rama `develop`
- [ ] Definir y documentar stack en `ARQUITECTURA.md`
- [ ] Crear `.env.example` sin secretos
- [ ] Setup local: Python venv, Node.js, Docker

**Validación:**
- ✅ `docker-compose up` debe iniciar backend, frontend y DB sin errores

---

#### Día 3-4: Ingesta de Datos (CRÍTICO)

**Tareas:**
- [ ] Descargar dataset del INE (22 XLSX)
- [ ] Estructurar `/data/raw`
- [ ] Crear `diccionario_variables.json` (mapeo código → etiqueta)
- [ ] Script Python que lee XLSX:
  - Lee todas las hojas
  - Valida esquema
  - Decodifica con diccionario
  - Genera `output/datos_decodificados.csv` (una muestra)
- [ ] Crear schema PostgreSQL (tabla `inscripciones`)
- [ ] Script carga datos en BD
- [ ] Verifica que sum(estudiantes) = 4.3M

**Validación:**
- ✅ Archivo pequeño se procesa sin errores
- ✅ 10 registros seleccionados se leen y se decodifican correctamente
- ✅ Si en XLSX ves `1` en sector, en BD debe verse "Público"

---

#### Día 5: Agregaciones y Métricas

**Tareas:**
- [ ] Crear tabla `resumen_departamento` (22 filas, 1 por depto)
  - Campos: total_estudiantes, aprobados, no_aprobados, retirados, tasa_aprobacion, tasa_desercion
- [ ] Crear tabla `resumen_urbano_rural` (2 filas)
- [ ] Crear tabla `resumen_sector` (2 filas: público/privado)
- [ ] Script que calcula todas las agregaciones
- [ ] Verificación: números cierran

**Validación:**
- ✅ Sumar resumen_departamento.total = 4.3M
- ✅ (aprobados + no_aprobados + retirados) = total en cada fila
- ✅ tasa_aprobacion está entre 0 y 100

---

### Semana 2: Backend y API

#### Día 6-7: FastAPI Setup

**Tareas:**
- [ ] Crear `backend/main.py` con FastAPI
- [ ] Setup conexión PostgreSQL (SQLAlchemy)
- [ ] Endpoint `/api/resumen` que retorna KPIs nacionales
- [ ] Endpoint `/api/departamentos` que lista todos con métricas
- [ ] Tests simples (curl o Postman)

**Validación:**
- ✅ `curl http://localhost:8000/api/resumen` retorna JSON válido
- ✅ Cifras coinciden con valores en BD

---

#### Día 8-9: Endpoints de Exploración

**Tareas:**
- [ ] Endpoint `/api/departamento/:id` (detalle)
- [ ] Endpoint `/api/comparativas?tipo=urbano_rural`
- [ ] Filtros genéricos: `?sector=publico&zona=rural` (reutilizable)
- [ ] Manejo de errores (404, 400)

**Validación:**
- ✅ Cambia filtros, resultados cambian
- ✅ Los números de un filtro coinciden con agregación manual

---

#### Día 10: Agente IA (Sin Alucinaciones)

**Tareas:**
- [ ] Diseñar prompt para Claude:
  ```
  Eres un asistente de análisis educativo. 
  Responde SOLO basándote en los datos que te proporciono.
  Si no tienes información, di "No tenemos esos datos".
  Nunca inventes cifras.
  ```
- [ ] Crear función `query_agente(pregunta: str)`:
  - Interpreta pregunta (¿es sobre aprobación? ¿deserción?)
  - Ejecuta SQL apropiado
  - Pasa contexto a Claude
  - Retorna respuesta + datos_usados
- [ ] Endpoint `/api/buscar` que llama esta función
- [ ] Test manual: hacer 5 preguntas, verificar que responde bien

**Validación:**
- ✅ Pregunta: "¿Cuál es la aprobación en Guatemala?"
  - Respuesta contiene cifra correcta
  - Identifica que es pregunta nacional
- ✅ Pregunta: "¿Cuál es el color del dinero en educación?"
  - Respuesta: "No tengo información sobre eso en los datos"

---

### Semana 3: Frontend

#### Día 11-12: React Setup + Vista Inicio

**Tareas:**
- [ ] Crear proyecto Next.js / React
- [ ] Setup conexión a backend (axios/fetch)
- [ ] Componente `Dashboard.jsx` (vista inicio)
  - 4 cards con KPIs (estudiantes, aprobación, urbano/rural, público/privado)
  - Cada card trae datos de `/api/resumen`
- [ ] Componente de análisis escrito (párrafo acompañante)
- [ ] Styling básico (Tailwind o Material-UI)

**Validación:**
- ✅ Cards se cargan y muestran números correctos
- ✅ Responsive en desktop y móvil

---

#### Día 13-14: Vista Departamentos

**Tareas:**
- [ ] Tabla interactiva con 22 departamentos
  - Ordenable por columnas
  - Clickeable (va a detalle)
- [ ] Componente `Filtros.jsx`:
  - Dropdowns para sector, zona, resultado
  - Actualiza tabla en tiempo real
- [ ] Gráfico de barras (Top 5 por indicador)

**Validación:**
- ✅ Tabla carga y ordena
- ✅ Cambia filtros, tabla se actualiza
- ✅ Las cifras en tabla coinciden con `/api/departamentos`

---

#### Día 15: Vista Análisis Temático

**Tareas:**
- [ ] Tabs para temas (urbano/rural, públco/privado, etc.)
- [ ] Gráficos comparativos (lado a lado)
- [ ] Análisis escrito para cada tema
- [ ] Opcional: mapa de Guatemala coloreado

**Validación:**
- ✅ Cada tab carga datos correctos
- ✅ Gráficos y texto son coherentes

---

### Semana 4: Integración y Pulido

#### Día 16-17: Chat Widget

**Tareas:**
- [ ] Componente `ChatAgent.jsx`
  - Historial de mensajes
  - Input de texto
  - Botones de preguntas sugeridas
- [ ] Llamadas a `/api/buscar`
- [ ] Mostrar respuesta + badge "Basado en datos"

**Validación:**
- ✅ Escribe pregunta, recibe respuesta en < 5 seg
- ✅ Respuesta es legible y correcta

---

#### Día 18-19: Documentación y Videos

**Tareas:**
- [ ] Completar `README.md`:
  - Qué hace la solución
  - Cómo instalarla localmente
  - Cómo ejecutar ingesta, backend, frontend
  - Cómo configurar credenciales de Claude API
- [ ] Crear `ARQUITECTURA.md`:
  - Decisiones técnicas
  - Por qué cada tecnología
  - Limitaciones conocidas
  - Cómo la IA se integra (RAG, prompting, etc.)
- [ ] Grabar Video 1 (Arquitectura, 3 min máx):
  - Muestra diagrama
  - Explica flujo de datos
  - Menciona tecnologías
- [ ] Grabar Video 2 (Funcionamiento, 3 min máx):
  - Recorre dashboard
  - Hace 3 preguntas al chat
  - Muestra cómo responde

**Validación:**
- ✅ Videos son claros, audio OK, pantalla legible
- ✅ README permite clonar y ejecutar sin help

---

#### Día 20: Testing y Reproducibilidad

**Tareas:**
- [ ] Verifica: clonar repo en limpio, seguir README, ¿funciona?
- [ ] Tests funcionales:
  - Ingesta: pequeño subset de datos
  - API: endpoints responden
  - Frontend: interfaces cargan
- [ ] Verificación de secretos: no hay credenciales en Git
- [ ] docker-compose.yml actualizado

**Validación:**
- ✅ Clon + `docker-compose up` = proyecto funcional

---

## 7. VALIDACIONES EN CADA ETAPA

### Validación de Ingesta (Etapa 1)

Antes de empezar backend, verifica:

- [ ] **Integridad:** Todos los 4.3M registros se cargaron (SELECT COUNT(*))
- [ ] **Decodificación:** 10 registros aleatorios se decodificaron correctamente
- [ ] **Cierre de números:** sum(total) por depto = 4.3M
- [ ] **Métricas:** (aprobados + no_aprobados + retirados) = total en cada fila
- [ ] **Rangos:** tasa_aprobacion, tasa_desercion ∈ [0, 100]
- [ ] **Zeros ficticios:** Código `9` se trata como "Ignorado" (visible en datos)

**Documento de evidencia:**
```
VALIDACION_INGESTA.txt:
- Total de registros: 4,300,XXX ✓
- Muestra de 10 registros decodificados: [PDF/imagen]
- Suma de estudiantes por depto: 4,300,XXX ✓
- Rango de tasas: [0-100] ✓
```

---

### Validación de Backend (Etapa 2)

Antes de tocar frontend, verifica:

- [ ] **Endpoints:** Todos retornan JSON válido en < 2 seg
- [ ] **Coherencia:** Cifras en `/api/resumen` coinciden con BD
- [ ] **Filtros:** Cambiar filtros cambia resultados correctamente
- [ ] **Agente:** Responde preguntas simples sin inventar
- [ ] **Errores:** Maneja 404, 500 gracefully

**Documento de evidencia:**
```
VALIDACION_API.txt:
- Endpoint /api/resumen:
  * Status: 200
  * Aprobación nacional: 87% (verificada en BD) ✓
- Endpoint /api/buscar "¿Aprobación en Guatemala?":
  * Respuesta: "La aprobación nacional fue 87%"
  * ¿Datos correctos? SÍ ✓
```

---

### Validación de Frontend (Etapa 3)

Antes de pitch, verifica:

- [ ] **Carga de datos:** Cards/tablas muestran números correctos
- [ ] **Responsivo:** Se ve bien en desktop (1920px), tablet (768px), móvil (375px)
- [ ] **Accesibilidad:** Contraste WCAG AA, textos legibles
- [ ] **Performance:** Carga en < 3 seg, cambios de filtro instantáneos
- [ ] **Chat:** Responde en < 5 seg, respuestas son legibles

**Documento de evidencia:**
```
VALIDACION_FRONTEND.txt:
- Dashboard carga en 2.3 seg ✓
- Tabla de departamentos ordena correctamente ✓
- Chat responde "¿Aprobación rural?" en 4 seg ✓
- Responsive en 3 tamaños verificado ✓
```

---

## 8. ESTRATEGIA DE PRESENTACIÓN (PITCH)

### Estructura de 5 Minutos

#### **00:00 - 00:30 | El Problema (30 seg)**
```
"4.3 millones de estudiantes guatemaltecos. Eso son 4.3 millones 
de registros sobre educación en 2024. Los datos existen, son públicos 
y gratuitos. Pero casi nadie los usa. ¿Por qué? 

Porque los datos vienen en código. "1" significa "Público", pero 
no lo sabes. "5" es "No promovido", pero está como número. 

Hicimos una herramienta que traduce esos códigos, calcula lo que falta,
y te deja hablar con los datos como si fueran una persona."
```

---

#### **00:30 - 02:00 | Qué Construyeron (90 seg)**
```
MOSTRAR: Dashboard cargado, en vivo.

"Esto es el dashboard. Acá ves:
- Estudiantes totales y tasa de aprobación (números grandes)
- Cómo es en el área urbana vs rural (diferencia clara)
- Público vs privado (otro contraste)

Pero no es solo gráficas. Cada vista tiene un párrafo que explica
qué significa. Por ejemplo: 'La aprobación fue 87%, pero varía 
mucho entre departamentos. Huehuetenango tiene la tasa más baja.'

[Hacer click en departamentos]

Acá ves los 22 departamentos ordenados, filtrados. 
[Cambiar filtro a "rural"]

¿Ves? Los números cambian. Ahora vemos solo estudiantes del área rural.

[Abrir chat]

Y por último: puedes hacer preguntas. 
[Escribir: 'Cuál es la tasa de deserción en el área rural?']
[Esperar respuesta]

El chat entiende tu pregunta, busca en los datos, y responde. 
No inventa. Si no tiene información, lo dice."
```

---

#### **02:00 - 04:00 | Cómo lo Hicieron (120 seg)**
```
"Ahora, técnicamente.

[Mostrar diagrama en diapositiva o lápiz]

Hay tres partes:

1. INGESTA: Un script Python que toma los 22 archivos XLSX,
   entiende que "1" es "Público", decodifica todo, calcula 
   las tasas de aprobación y deserción, y guarda en una base de datos.
   
   Esto fue lo más crítico. Si esto falla, todo falla.
   
2. BACKEND: Una API (FastAPI) que ofrece tres cosas:
   - Datos listos para visualizar (GET /api/departamentos)
   - Filtros en tiempo real 
   - Un endpoint de búsqueda que conecta con Claude (IA).
   
   Claude no memoriza los 4.3M registros. En su lugar, la API 
   ejecuta la pregunta en SQL, trae contexto real, y Claude 
   escribe la respuesta. Así no inventa.
   
3. FRONTEND: React + gráficas interactivas. El usuario elige 
   departamento, sector, zona. Los números se actualizan. 
   Hace preguntas y obtiene respuestas basadas en datos.

[Pausar]

¿Por qué lo armamos así? Porque queremos que el usuario
no solo vea gráficas, sino que entienda. Que haga preguntas. 
Y que confíe en la respuesta porque sabe de dónde viene."
```

---

#### **04:00 - 05:00 | Aprendizajes y Pendientes (60 seg)**
```
"Aprendimos tres cosas:

1. Los datos educativos son complejos. Validarlos fue más de 
   lo que pensamos. Pero fue necesario.

2. Integrar IA sin que invente fue el reto principal. 
   Usamos RAG: la IA no memoriza datos, busca en BD y responde.

3. La narrativa importa más que las gráficas. Un párrafo que 
   explique qué significa un número vale más que 10 gráficas 
   que nadie entiende.

Si tuviéramos más tiempo:
- Comparación temporal (¿2023 vs 2024?)
- Análisis predictivo (tendencias)
- Exportar reportes personalizados

Pero con lo que tenemos, cualquiera —un periodista, una autoridad, 
un docente— puede abrir esto y entender qué pasa con la educación 
en su departamento en 20 minutos."
```

---

### Preparación Técnica del Pitch

**Antes de entrar:**
- [ ] Dashboard cargado en navegador (sección inicio, visible)
- [ ] Backend respondiendo (sin errores)
- [ ] Chat listo para una pregunta de prueba
- [ ] Diapositiva con diagrama (o lápiz para dibujar)
- [ ] Video de arquitectura descargado (si internet falla)

**Durante:**
- Habla claro, lento, pausado
- "Mientras se carga..." es mejor que silencio incómodo
- Traduce jerga técnica: "RAG" → "la IA no memoriza, busca en datos"
- Si algo falla: "Esto pasó durante desarrollo, lo solucionamos aquí"

**Preguntas Esperadas de Jueces (Anticipa):**

| Pregunta | Respuesta |
|----------|-----------|
| "¿Cómo garantizan que las cifras son correctas?" | Validamos contra el dataset original. Sumar todos los departamentos = 4.3M ✓ |
| "¿Qué hace el agente de IA exactamente?" | Recibe pregunta → busca en BD → le pasa contexto a Claude → Claude responde. No inventa. |
| "¿Por qué no usan una base de datos en la nube?" | Para reproducibilidad local y control. Pero es escalable. |
| "¿Cuál fue lo más difícil?" | Decodificar correctamente. Si una variable se interpreta mal, todo sale mal. |
| "¿Usaron IA para generar código?" | [Sé honesto] Usamos Claude para [componentes específicos]. Pero entendemos y controlamos todo. |

---

## 9. CHECKLIST FINAL

Antes de hacer submit:

### Código
- [ ] Repositorio público en GitHub
- [ ] README con instrucciones (clone + docker-compose up = funciona)
- [ ] ARQUITECTURA.md con decisiones técnicas
- [ ] `.env.example` sin secretos
- [ ] `.gitignore` excluye datos grandes, dependencias, secretos
- [ ] Rama main limpia (sin cambios a mitad)

### Audiovisual
- [ ] Video 1 (Arquitectura): 3 min máx, audio claro, explicación coherente
- [ ] Video 2 (Funcionamiento): 3 min máx, se ve el dashboard y el chat en acción

### Reproduciblidad
- [ ] Clona en limpio, sigue README, ¿funciona?
- [ ] Sin dependencias no documentadas
- [ ] Sin directorios hardcodeados (`C:\Users\...`)

### Evidencia de Comprensión
- [ ] Puedes explicar el flujo de datos: entrada → ingesta → BD → API → frontend
- [ ] Sabes por qué cada tecnología: FastAPI (rápido, fácil), PostgreSQL (relacional), React (interactivo)
- [ ] Comprendes el diseño: por qué separar ingesta del frontend, por qué RAG en el agente
- [ ] Puedes responder qué hizo IA y qué hiciste tú

### Pitch
- [ ] Ensayaste mínimo una vez completo con reloj
- [ ] Tienes 30 seg para problema, 90 para demo, 120 para arquitectura
- [ ] Anticipaste preguntas de jueces
- [ ] Sabes qué decir si algo falla en vivo

---

## 10. REFERENCIAS Y RECURSOS

### Documentación Oficial
- Dataset: https://datos.ine.gob.gt/dataset/educacion-formal-2024
- Diccionario de variables: Incluido en el dataset

### Librerías y Frameworks
- **Backend:** FastAPI (docs: fastapi.tiangolo.com)
- **Frontend:** React (react.dev) o Next.js (nextjs.org)
- **Datos:** Pandas (pandas.pydata.org), NumPy
- **BD:** PostgreSQL (postgresql.org), SQLAlchemy (sqlalchemy.org)
- **Viz:** Plotly.js, Recharts
- **IA:** Claude API (Anthropic, claude.ai/docs)

### Conceptos Clave
- **RAG (Retrieval-Augmented Generation):** IA que busca contexto antes de responder
- **Ingesta de datos:** ETL (Extract, Transform, Load)
- **Prompting:** Cómo instruir a Claude para respuestas confiables

---

## 11. NOTAS FINALES

### Filosofía del Proyecto

Este no es un dashboard hermoso ni código perfecto. Es una **solución que funciona, que se entiende, que confías**.

- **Haz lo mínimo bien** en lugar de mucho a medias.
- **Documenta decisiones.** "¿Por qué FastAPI y no Django?" Cuenta.
- **Sé honesto con IA.** "Generé X con Claude, Y lo escribí yo, Z lo debuggeamos juntos."
- **Valida todo.** Si una cifra aparece en pantalla, debe ser verificable contra datos crudos.

### Timeline Realista

- Semana 1: Ingesta (lo más crítico)
- Semana 2: API y agente
- Semana 3: Frontend bonito
- Semana 4: Pulido, videos, documentación

Si corres tiempo corto: **sacrifica frontend bonito antes que ingesta o agente.**

### Indicadores de Éxito

✅ **Mínimo:** Dashboard + Chat funcionan, datos coherentes, código documentado

✅ **Bien:** Además: análisis escrito, filtros interactivos, videos claros

✅ **Excelente:** Además: narrativa convincente, código limpio, demostración flawless en pitch

---

**Última actualización:** [Hoy]  
**Autores:** Tu equipo  
**Estado:** En desarrollo
