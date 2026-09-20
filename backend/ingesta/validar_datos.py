import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "educacion.db"
DOCS_VALIDACION_PATH = BASE_DIR / "VALIDACION_INGESTA.md"

def validar_consistencia():
    print("=== VALIDACIÓN TÉCNICA DE INGESTA Y BASE DE DATOS ===")
    
    if not DB_PATH.exists():
        print(f"Error: No existe la base de datos en {DB_PATH}")
        return False

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    checks = []

    # 1. Validar Resumen Nacional
    cursor.execute("SELECT * FROM resumen_nacional LIMIT 1;")
    nacional = dict(cursor.fetchone())
    tot_nac = nacional["total_estudiantes"]
    apr_nac = nacional["aprobados"]
    no_apr_nac = nacional["no_aprobados"]
    ret_nac = nacional["retirados"]
    tasa_apr_nac = nacional["tasa_aprobacion"]
    tasa_des_nac = nacional["tasa_desercion"]

    check_nac_suma = (apr_nac + no_apr_nac + ret_nac == tot_nac)
    checks.append({
        "descripcion": "Cierre de suma nacional (Aprobados + No Aprobados + Retirados == Total)",
        "resultado": "PASÓ" if check_nac_suma else "FALLÓ",
        "detalle": f"{apr_nac:,} + {no_apr_nac:,} + {ret_nac:,} = {tot_nac:,}"
    })

    check_nac_rango = (0 <= tasa_apr_nac <= 100) and (0 <= tasa_des_nac <= 100)
    checks.append({
        "descripcion": "Tasas nacionales en rango valido [0%, 100%]",
        "resultado": "PASÓ" if check_nac_rango else "FALLÓ",
        "detalle": f"Aprobación: {tasa_apr_nac}%, Deserción: {tasa_des_nac}%"
    })

    # 2. Validar Departamentos
    cursor.execute("SELECT * FROM resumen_departamento;")
    deptos = [dict(row) for row in cursor.fetchall()]
    
    check_cant_deptos = (len(deptos) == 22)
    checks.append({
        "descripcion": "Total de departamentos registrados (exactamente 22)",
        "resultado": "PASÓ" if check_cant_deptos else "FALLÓ",
        "detalle": f"{len(deptos)} departamentos encontrados"
    })

    suma_deptos = sum(d["total_estudiantes"] for d in deptos)
    check_suma_deptos = (suma_deptos == tot_nac)
    checks.append({
        "descripcion": "Suma de estudiantes por departamento coincide con el Total Nacional",
        "resultado": "PASÓ" if check_suma_deptos else "FALLÓ",
        "detalle": f"Suma Deptos: {suma_deptos:,} vs Total Nacional: {tot_nac:,}"
    })

    deptos_invalidos = []
    for d in deptos:
        tot_d = d["total_estudiantes"]
        suma_partes = d["aprobados"] + d["no_aprobados"] + d["retirados"]
        if tot_d != suma_partes:
            deptos_invalidos.append(d["departamento"])
        if not (0 <= d["tasa_aprobacion"] <= 100 and 0 <= d["tasa_desercion"] <= 100):
            deptos_invalidos.append(f"{d['departamento']} (tasa fuera de rango)")

    check_deptos_consistencia = (len(deptos_invalidos) == 0)
    checks.append({
        "descripcion": "Consistencia individual de cada departamento (suma interna y tasas)",
        "resultado": "PASÓ" if check_deptos_consistencia else "FALLÓ",
        "detalle": "Todos los 22 departamentos son consistentes" if check_deptos_consistencia else f"Errores en: {', '.join(deptos_invalidos)}"
    })

    # 3. Validar Área (Urbana vs Rural)
    cursor.execute("SELECT * FROM resumen_area;")
    areas = [dict(row) for row in cursor.fetchall()]
    suma_areas = sum(a["total_estudiantes"] for a in areas)
    check_areas = (suma_areas == tot_nac)
    checks.append({
        "descripcion": "Suma de áreas Urbana y Rural coincide con Total Nacional",
        "resultado": "PASÓ" if check_areas else "FALLÓ",
        "detalle": f"Total Áreas: {suma_areas:,} vs Total Nacional: {tot_nac:,}"
    })

    # 4. Validar Sector
    cursor.execute("SELECT * FROM resumen_sector;")
    sectores = [dict(row) for row in cursor.fetchall()]
    suma_sectores = sum(s["total_estudiantes"] for s in sectores)
    check_sectores = (suma_sectores == tot_nac)
    checks.append({
        "descripcion": "Suma por sectores (Oficial, Privado, Cooperativa, Municipal) coincide con Total Nacional",
        "resultado": "PASÓ" if check_sectores else "FALLÓ",
        "detalle": f"Total Sectores: {suma_sectores:,} vs Total Nacional: {tot_nac:,}"
    })

    # 5. Validar Sexo
    cursor.execute("SELECT * FROM resumen_sexo;")
    sexos = [dict(row) for row in cursor.fetchall()]
    suma_sexos = sum(s["total_estudiantes"] for s in sexos)
    check_sexos = (suma_sexos == tot_nac)
    checks.append({
        "descripcion": "Suma por sexo (Hombres + Mujeres) coincide con Total Nacional",
        "resultado": "PASÓ" if check_sexos else "FALLÓ",
        "detalle": f"Total Sexos: {suma_sexos:,} vs Total Nacional: {tot_nac:,}"
    })

    # 6. Validar Muestra de Inscripciones
    cursor.execute("SELECT COUNT(*) as total FROM inscripciones_muestra;")
    total_muestra = cursor.fetchone()["total"]
    checks.append({
        "descripcion": "Tabla de muestra de inscripciones disponible para consultas y pruebas del Agente IA",
        "resultado": "PASÓ" if total_muestra > 0 else "FALLÓ",
        "detalle": f"{total_muestra} registros de muestra disponibles"
    })

    conn.close()

    # Generar Documento de Evidencia VALIDACION_INGESTA.md
    md_content = [
        "# Evidencia de Validación Técnica - Ingesta y Base de Datos (Data Engineer)",
        "",
        "Este documento certifica la consistencia estadística y matemática del modelo de datos para el **Hackathon AI Builders GT**.",
        "",
        "## Resultados de los Checks de Calidad",
        "",
        "| Check | Estado | Detalle Técnico |",
        "|---|---|---|"
    ]

    todo_ok = True
    for c in checks:
        if c["resultado"] != "PASÓ":
            todo_ok = False
        md_content.append(f"| {c['descripcion']} | **{c['resultado']}** | {c['detalle']} |")

    md_content.extend([
        "",
        "## Resumen de Métricas Clave Nacionales (2024)",
        f"- **Total Estudiantes Inscritos:** {tot_nac:,}",
        f"- **Total Aprobados:** {apr_nac:,} ({tasa_apr_nac}%)",
        f"- **Total No Aprobados (Repitencia):** {no_apr_nac:,} ({nacional['tasa_repitencia']}%)",
        f"- **Total Retirados (Deserción Escolar):** {ret_nac:,} ({tasa_des_nac}%)",
        "",
        "## Departamentos con Mayor y Menor Tasa de Aprobación",
        ""
    ])

    deptos_sorted_apr = sorted(deptos, key=lambda x: x["tasa_aprobacion"], reverse=True)
    md_content.append("### Top 3 Mayor Aprobación:")
    for d in deptos_sorted_apr[:3]:
        md_content.append(f"1. **{d['departamento']}**: {d['tasa_aprobacion']}% aprobación (Total: {d['total_estudiantes']:,})")

    md_content.append("")
    md_content.append("### Top 3 Menor Aprobación (Mayor Vulnerabilidad):")
    for d in deptos_sorted_apr[-3:]:
        md_content.append(f"1. **{d['departamento']}**: {d['tasa_aprobacion']}% aprobación | Deserción: {d['tasa_desercion']}%")

    with open(DOCS_VALIDACION_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content) + "\n")

    print(f"\nInforme de validacion generado con exito en: {DOCS_VALIDACION_PATH}")
    for c in checks:
        print(f"[{c['resultado']}] {c['descripcion']} -> {c['detalle']}")

    return todo_ok

if __name__ == "__main__":
    validar_consistencia()
