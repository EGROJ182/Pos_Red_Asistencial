import json

# Datos de prueba
data_chart_reps = {
    "Antioquia": {"TERAPIA RESPIRATORIA": 26, "CIRUGÍA UROLÓGICA": 18},
    "Bogotá": {"TERAPIA RESPIRATORIA": 12, "CIRUGÍA UROLÓGICA": 5},
    "Valle del Cauca": {"TERAPIA RESPIRATORIA": 15, "CIRUGÍA UROLÓGICA": 10}
}

# 1️⃣ Obtener lista de departamentos (labels)
departamentos = list(data_chart_reps.keys())

# 2️⃣ Obtener lista de tipos de servicio únicos
tipos_servicio = sorted({tipo for dpto in data_chart_reps.values() for tipo in dpto})

# 3️⃣ Construir datasets para Chart.js
chart_reps = []
for tipo in tipos_servicio:
    chart_reps.append({
        "label": tipo,
        "data": [data_chart_reps[dpto].get(tipo, 0) for dpto in departamentos],
        "backgroundColor": f"rgba({hash(tipo) % 255}, {100 + hash(tipo) % 155}, {200 - hash(tipo) % 100}, 0.6)"
    })

# 4️⃣ Crear JSON con estructura correcta
chart_reps_json = json.dumps({"labels": departamentos, "datasets": chart_reps}, ensure_ascii=False)

# 📌 Verificar salida
print(chart_reps_json)
