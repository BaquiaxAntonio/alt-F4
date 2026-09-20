# Plan de Trabajo del Equipo - SPRINT DE 3 HORAS (Hackathon)

Dado que el desarrollo completo se debe ejecutar en **solo 3 horas**, la clave es el **desarrollo en paralelo estricto**, el uso de **datos mockeados (falsos/de prueba)** al principio para no bloquear al frontend, y la creación de un **MVP (Producto Mínimo Viable)**.

El stack tecnológico se mantiene (React/Next.js, FastAPI, PostgreSQL/SQLite, Claude/GPT-4), pero el ritmo es intensivo.

## Roles Asignados

1. **Persona 1: Data Engineer** (Ingesta exprés y Base de Datos)
2. **Persona 2: Backend Developer** (API y conexión rápida)
3. **Persona 3: Frontend Developer (UI/UX)** (Layout y componente del Chat)
4. **Persona 4: Frontend Developer (Data Viz)** (Gráficos interactivos)
5. **Persona 5: AI Engineer & DevOps** (Prompting, Docker y Entregables)

---

## Cronograma de Ejecución (3 Horas)

### Hora 1: Setup Base y MVP (0:00 - 1:00)
*Objetivo: Todos trabajando sin bloquear a nadie.*

- **Persona 1 (Data Engineer):** 
  - Limpiar y decodificar solo un subconjunto crítico del dataset (ej. totales nacionales y un par de departamentos) usando Pandas.
  - Exportar estos primeros datos limpios a SQLite o PostgreSQL rápido.
- **Persona 2 (Backend Developer):**
  - Levantar `FastAPI` de inmediato.
  - Crear endpoints **mockeados** (`/api/resumen`, `/api/departamentos`) devolviendo JSONs fijos. Entregar estos JSONs al Frontend al minuto 15.
  - Conectar los endpoints a la base de datos de la Persona 1 al final de la hora.
- **Persona 3 (Frontend Developer UI/UX):**
  - Iniciar proyecto (`npx create-next-app` o Vite), instalar Tailwind/Shadcn.
  - Construir layout principal (Navbar, estructura del Dashboard).
  - Integrar los JSONs mockeados de la Persona 2.
- **Persona 4 (Frontend Developer Data Viz):**
  - Instalar Recharts o Plotly.js.
  - Crear los componentes de gráficos de barras y líneas usando los JSONs mockeados.
- **Persona 5 (AI Engineer & DevOps):**
  - Crear repositorio en GitHub e invitar al equipo.
  - Escribir script standalone en Python para probar la API de Claude/GPT-4 enviando el contexto (RAG básico).
  - Compartir `.env.example` y asegurar que todos puedan levantar su entorno.

### Hora 2: Integración e Interactividad (1:00 - 2:00)
*Objetivo: Conectar el Frontend al Backend real y hacer funcionar el Agente IA.*

- **Persona 1 (Data Engineer):**
  - Procesar el resto de los archivos XLSX y subirlos a la base de datos.
  - Generar vistas o agrupaciones rápidas para "sectores" y "zonas" (Urbano/Rural).
- **Persona 2 (Backend Developer):**
  - Integrar el script de IA (hecho por Persona 5) dentro del endpoint POST `/api/buscar`.
  - Reemplazar los endpoints mockeados por consultas SQL reales a la base de datos completa.
- **Persona 3 (Frontend Developer UI/UX):**
  - Cambiar peticiones mockeadas por llamadas `fetch`/`axios` a la API real.
  - Construir la UI del ChatBot (Widget) y conectarlo al endpoint `/api/buscar`.
- **Persona 4 (Frontend Developer Data Viz):**
  - Implementar los dropdowns de Filtros (Departamento, Rural/Urbano).
  - Hacer que los gráficos se actualicen dinámicamente al cambiar los filtros y recargar datos de la API.
- **Persona 5 (AI Engineer & DevOps):**
  - Ajustar el prompt de Claude para reducir tiempo de respuesta y evitar alucinaciones con base en pruebas.
  - Empezar a redactar el `README.md` y `ARQUITECTURA.md`.

### Hora 3: Pulido, Validación y Entregables (Pitch) (2:00 - 3:00)
*Objetivo: Que el proyecto no falle en la presentación y generar los videos requeridos.*

- **Persona 1 (Data Engineer):**
  - Validación express: Revisar la UI y confirmar que las cifras (ej. "Tasa de aprobación") hacen sentido y no hay errores de cálculo.
- **Persona 2 (Backend Developer):**
  - Fixes rápidos (manejo de errores de conexión, caídas de la DB).
  - Optimizar tiempos de respuesta si algo tarda más de 2 segundos.
- **Persona 3 (Frontend Developer UI/UX):**
  - Pulido de estilos visuales (colores, padding, estado de "Cargando..." en el chat).
  - Comprobación rápida de responsividad (que no se rompa si cambian el tamaño de la ventana).
- **Persona 4 (Frontend Developer Data Viz):**
  - Verificar tooltips de los gráficos.
  - Manejo de estados vacíos (¿Qué pasa si un filtro no tiene datos?).
- **Persona 5 (AI Engineer & DevOps):**
  - Subir la versión final de la aplicación (Despliegue rápido en Vercel/Render).
  - **Grabar Video 1 (Arquitectura)** y **Video 2 (Funcionamiento/Demo)**. 
  - Asegurar que el repositorio en GitHub está público, limpio y contiene las instrucciones para ejecutar.

---

## Resumen de Responsabilidades y Entregables Clave

| Miembro | Rol | Entregable Clave en las 3 Horas |
|---|---|---|
| **Persona 1** | Data Engineer | Script de limpieza y Base de Datos funcional con cálculos correctos. |
| **Persona 2** | Backend Dev | Endpoints en FastAPI (Resumen, Deptos, Búsqueda IA). |
| **Persona 3** | Frontend (UI) | Aplicación levantada, diseño general y chat integrado. |
| **Persona 4** | Frontend (Data) | Filtros funcionales y gráficas dinámicas que reaccionan. |
| **Persona 5** | AI / DevOps | Repo listo, Endpoint de Claude afinado, Docs y Videos. |
