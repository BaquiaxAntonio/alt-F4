# Evidencia de Validación Técnica - Ingesta y Base de Datos (Data Engineer)

Este documento certifica la consistencia estadística y matemática del modelo de datos para el **Hackathon AI Builders GT**.

## Resultados de los Checks de Calidad

| Check | Estado | Detalle Técnico |
|---|---|---|
| Cierre de suma nacional (Aprobados + No Aprobados + Retirados == Total) | **PASÓ** | 3,978,836 + 417,160 + 227,004 = 4,623,000 |
| Tasas nacionales en rango valido [0%, 100%] | **PASÓ** | Aprobación: 86.07%, Deserción: 4.91% |
| Total de departamentos registrados (exactamente 22) | **PASÓ** | 22 departamentos encontrados |
| Suma de estudiantes por departamento coincide con el Total Nacional | **PASÓ** | Suma Deptos: 4,623,000 vs Total Nacional: 4,623,000 |
| Consistencia individual de cada departamento (suma interna y tasas) | **PASÓ** | Todos los 22 departamentos son consistentes |
| Suma de áreas Urbana y Rural coincide con Total Nacional | **PASÓ** | Total Áreas: 4,623,000 vs Total Nacional: 4,623,000 |
| Suma por sectores (Oficial, Privado, Cooperativa, Municipal) coincide con Total Nacional | **PASÓ** | Total Sectores: 4,623,000 vs Total Nacional: 4,623,000 |
| Suma por sexo (Hombres + Mujeres) coincide con Total Nacional | **PASÓ** | Total Sexos: 4,623,000 vs Total Nacional: 4,623,000 |
| Tabla de muestra de inscripciones disponible para consultas y pruebas del Agente IA | **PASÓ** | 100 registros de muestra disponibles |

## Resumen de Métricas Clave Nacionales (2024)
- **Total Estudiantes Inscritos:** 4,623,000
- **Total Aprobados:** 3,978,836 (86.07%)
- **Total No Aprobados (Repitencia):** 417,160 (9.02%)
- **Total Retirados (Deserción Escolar):** 227,004 (4.91%)

## Departamentos con Mayor y Menor Tasa de Aprobación

### Top 3 Mayor Aprobación:
1. **Guatemala**: 90.0% aprobación (Total: 920,500)
1. **Sacatepéquez**: 90.0% aprobación (Total: 98,400)
1. **Quetzaltenango**: 89.0% aprobación (Total: 245,800)

### Top 3 Menor Aprobación (Mayor Vulnerabilidad):
1. **Quiché**: 83.03% aprobación | Deserción: 6.0%
1. **Huehuetenango**: 81.0% aprobación | Deserción: 7.5%
1. **Alta Verapaz**: 80.0% aprobación | Deserción: 7.5%
