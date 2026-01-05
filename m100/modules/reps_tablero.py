from django.shortcuts import render
from django.template.loader import render_to_string
from ..models.models_reps import reps
from ..modules.filters import apply_filters_reps
from ..models.models_dane import dane_data
from django.http import JsonResponse
from django.db.models import Count, F
from django.db.models.functions import Concat
from django.db.models import Q
from django.core.paginator import Paginator
import json

def repsInfo(request):
    dane = dane_data.objects.all()
    dane_dpto = dane.values('departamento').distinct().order_by('departamento')
    reps_data = reps.objects.using('dataTarifas').all()
    # Aplicar filtros
    reps_data = apply_filters_reps(reps_data, request)

    # Datos Proveedores Reps
    proveedores = reps_data.values('nit', 'nombre').distinct().order_by('nit')
    reps_sede = reps_data.values('serv_codigo', 'serv_nombre').distinct().order_by('serv_codigo')
    departamentos = reps_data.values('departamento').distinct().order_by('departamento')
    municipios_sede = reps_data.values('municipio').distinct().order_by('municipio')

    # Datos para mapa municipios por departamento reps
    prestadores_por_municipio = (
        reps_data.values('departamento')
        .annotate(total=Count(Concat(F('departamento'),F('municipio')), distinct=True))
        .order_by('-total')
    )

    # Datos para la torta prestadores por departamento
    prestadores_por_depto = (
        reps_data.values('departamento')
        .annotate(total=Count('nit', distinct=True))
        .order_by('-total')
    )
    suma_pres_dpto = sum(x['total'] for x in prestadores_por_depto)

    dep_dict = {}
    for item in prestadores_por_depto:
        dep_dict[item['departamento']] = item['total']

    full_data = []
    for d in dane_dpto:
        depto = d['departamento']
        # Buscamos el total en dep_dict, si no existe => 0
        total = dep_dict.get(depto, 0)
        full_data.append({'departamento': depto, 'total': total})

    chart_data = {
        'labels': [item['departamento'] for item in full_data],
        'data': [item['total'] for item in full_data],
    }
    chart_json = json.dumps(chart_data)

    # Datos para la torta sedes por departamento
    sedes_por_depto = (
        reps_data.values('departamento')
        .annotate(total=Count(Concat(F('codigo_de_habilitacion'),F('numero_sede')), distinct=True))
        .order_by('-total')
    )

    suma_sedes_dpto = sum(x['total'] for x in sedes_por_depto)

    dep_sedes_dict = {}
    for item in sedes_por_depto:
        dep_sedes_dict[item['departamento']] = item['total']

    full_data_sedes = []
    for d in dane_dpto:
        depto_sedes = d['departamento']
        # Buscamos el total en dep_dict, si no existe => 0
        total = dep_sedes_dict.get(depto_sedes, 0)
        full_data_sedes.append({'departamento': depto_sedes, 'total': total})

    chart_data_sedes = {
        'labels': [item['departamento'] for item in full_data_sedes],
        'data': [item['total'] for item in full_data_sedes],
    }
    chart_sedes_json = json.dumps(chart_data_sedes)

    # Datos para mapa reps por departamento
    reps_depto = (
        reps_data.values('departamento')
        .annotate(total=Count('serv_codigo', distinct=True))
        .order_by('-total')
    )
    
    #Datos para barras por dpto
    reps_por_departamento = (
        reps_data.values('departamento', 'serv_nombre')  # Agrupar por dpto y tipo de servicio
        .annotate(total_reps=Count('serv_codigo'))  # Contar los REPS por cada tipo
        .order_by('departamento', 'serv_nombre')  # Ordenar por dpto y servicio
    )
    # 3) Crear diccionario base con TODOS los dptos
    data_chart_reps = {d['departamento']: {} for d in dane_dpto}
    
    # 4) Llenar ese diccionario con la info de reps_por_departamento
    for item in reps_por_departamento:
        dpto = item['departamento']
        tipo = item['serv_nombre']
        total = item['total_reps']
        # Solo asignamos si el dpto está en DANE
        if dpto in data_chart_reps:
            data_chart_reps[dpto][tipo] = total

    # 5) Construir la lista de departamentos (labels)
    departamentos_reps = list(data_chart_reps.keys())  # ['Amazonas','Antioquia','Arauca',...]
    
    # 6) Construir la lista de tipos de servicio (serv_nombre) únicos
    #    Buscando en los valores del diccionario
    tipos_servicio = sorted({tipo for dict_serv in data_chart_reps.values() for tipo in dict_serv})
    # Ejemplo: ['CIRUGÍA UROLÓGICA', 'TERAPIA RESPIRATORIA', ...]

    # 7) Construir datasets para Chart.js
    #    Cada "tipo" será un dataset distinto
    chart_reps = []
    for tipo in tipos_servicio:
        dataset = {
            "label": tipo,
            "data": [data_chart_reps[dpto].get(tipo, 0) for dpto in departamentos_reps],
            "backgroundColor": f"rgba({hash(tipo) % 255}, {100 + hash(tipo) % 155}, {200 - hash(tipo) % 100}, 0.6)"
        }
        chart_reps.append(dataset)

    # 8) Estructura final para Chart.js
    #    {
    #      "labels": [ "Amazonas","Antioquia","Arauca",... ],
    #      "datasets": [
    #         { "label": "CIRUGÍA UROLÓGICA", "data": [...], ... },
    #         { "label": "TERAPIA RESPIRATORIA", "data": [...], ... },
    #         ...
    #      ]
    #    }
    chart_reps_json = json.dumps({
        "labels": departamentos_reps,
        "datasets": chart_reps
    })

    return proveedores, chart_json, chart_reps_json, suma_pres_dpto, chart_sedes_json, suma_sedes_dpto, prestadores_por_depto, prestadores_por_municipio, sedes_por_depto, reps_depto, reps_sede, departamentos, municipios_sede, reps_data

# context = {
#     'prov_c': proveedores,
#     'chart': chart_json,
#     'chart_reps': chart_reps_json,
#     'suma_chart': suma_pres_dpto,
#     'chart_sedes': chart_sedes_json,
#     'suma_chart_sedes': suma_sedes_dpto,
# }