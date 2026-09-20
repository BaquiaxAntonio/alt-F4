"""
Script de pruebas rápidas para la API.
Verifica que los endpoints principales respondan correctamente.

Uso:
  python backend/test_api.py

Requiere que el backend esté corriendo: uvicorn backend.main:app --reload
"""
import json
import sys

import httpx

BASE_URL = "http://localhost:8000"


def check(label: str, response: httpx.Response, expected_status: int = 200):
    status = "✅" if response.status_code == expected_status else "❌"
    print(f"\n{status} {label}")
    print(f"   Status: {response.status_code}")
    try:
        data = response.json()
        # Mostrar solo las primeras claves del JSON
        if isinstance(data, dict):
            preview = {k: str(v)[:60] for k, v in list(data.items())[:5]}
        elif isinstance(data, list):
            preview = f"[Lista con {len(data)} elementos]"
        else:
            preview = str(data)[:200]
        print(f"   Respuesta: {json.dumps(preview, ensure_ascii=False, indent=6)}")
    except Exception:
        print(f"   Body: {response.text[:200]}")


def main():
    print("=" * 60)
    print("VALIDACIÓN API - Educación Guatemala")
    print("=" * 60)

    with httpx.Client(timeout=30.0) as c:
        # 1. Root
        check("GET / (info)", c.get(f"{BASE_URL}/"))

        # 2. Health
        check("GET /api/health", c.get(f"{BASE_URL}/api/health"))

        # 3. Resumen nacional
        r = c.get(f"{BASE_URL}/api/resumen")
        check("GET /api/resumen", r)
        if r.status_code == 200:
            data = r.json()
            print(f"   → Total estudiantes: {data.get('total_estudiantes', 'N/D'):,}")
            print(f"   → Tasa aprobación: {data.get('tasa_aprobacion_promedio', 'N/D')}%")

        # 4. Departamentos
        r = c.get(f"{BASE_URL}/api/departamentos")
        check("GET /api/departamentos", r)
        if r.status_code == 200:
            deptos = r.json()
            print(f"   → Departamentos retornados: {len(deptos)}")
            if deptos:
                print(f"   → Primero: {deptos[0]['departamento']} - {deptos[0]['tasa_aprobacion']}%")

        # 5. Departamento específico
        check(
            "GET /api/departamento/Guatemala",
            c.get(f"{BASE_URL}/api/departamento/Guatemala"),
        )

        # 6. Comparativas - urbano/rural
        check(
            "GET /api/comparativas?tipo=urbano_rural",
            c.get(f"{BASE_URL}/api/comparativas", params={"tipo": "urbano_rural"}),
        )

        # 7. Comparativas - sector
        check(
            "GET /api/comparativas?tipo=sector",
            c.get(f"{BASE_URL}/api/comparativas", params={"tipo": "sector"}),
        )

        # 8. Agente IA - pregunta básica
        print("\n--- Prueba del Agente IA ---")
        r = c.post(
            f"{BASE_URL}/api/buscar",
            json={"pregunta": "¿Cuál es la tasa de aprobación nacional?"},
        )
        check("POST /api/buscar (aprobación nacional)", r)
        if r.status_code == 200:
            data = r.json()
            print(f"   → Intenciones: {data.get('intenciones_detectadas')}")
            print(f"   → Confianza: {data.get('confianza')}")
            print(f"   → Respuesta: {data.get('respuesta', '')[:150]}...")

        # 9. Agente IA - pregunta fuera de alcance
        r = c.post(
            f"{BASE_URL}/api/buscar",
            json={"pregunta": "¿Cuál es el precio del dólar hoy?"},
        )
        check("POST /api/buscar (pregunta sin datos)", r)

        # 10. Filtros en departamentos
        r = c.get(
            f"{BASE_URL}/api/departamentos",
            params={"area": "Rural", "orden": "tasa_desercion"},
        )
        check("GET /api/departamentos?area=Rural&orden=tasa_desercion", r)

    print("\n" + "=" * 60)
    print("Validación completa.")
    print("Si ves ❌, revisa que la ingesta se haya ejecutado.")
    print("=" * 60)


if __name__ == "__main__":
    main()
