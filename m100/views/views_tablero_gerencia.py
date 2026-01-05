from datetime import date, datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from django.template.loader import render_to_string
from ..models.models_tablero_gerencia import Tablero
from ..models.models_dane import dane_data
from ..modules.alert import alert
from django.http import JsonResponse
from django.db.models import Count, F
from django.db.models.functions import Concat
from django.db.models import Q
from ..modules.filters import apply_filters_tablero
from ..modules.reps_tablero import repsInfo
from ..modules.mapas import mapa2
import json

def dashboard(request):
    proveedores_contratados = Tablero.objects.all().values()
    dane = dane_data.objects.all()
    dane_dpto = dane.values('departamento').distinct().order_by('departamento')

    # Aplicar filtros
    proveedores_contratados, filtros_aplicados = apply_filters_tablero(proveedores_contratados, request)
    paginator_data = Paginator(proveedores_contratados, 100)
    page_number_data = request.GET.get('page')
    data_page = paginator_data.get_page(page_number_data)

    # Sucursales
    sucursales = Tablero.objects.values_list('sucursal', flat=True).distinct().order_by('sucursal')
    # Años
    years = Tablero.objects.values_list('year_contrato', flat=True).distinct().order_by('year_contrato')
    # Números Contratos
    numero_contrato = Tablero.objects.values_list('numero_contrato', flat=True).distinct().order_by('numero_contrato')
    # Supervisores
    supervisores = Tablero.objects.values_list('supervisor', flat=True).distinct().order_by('supervisor')
    # Categorias Cuentas Médicas
    categorias_cuentas_medicas = Tablero.objects.values_list('categoria_cuentas_medicas', flat=True).distinct().order_by('categoria_cuentas_medicas')
    # Números Sedes
    numeros_sedes = Tablero.objects.values_list('numero_sede', flat=True).distinct().order_by('numero_sede')
    # Departamentos
    dptos = Tablero.objects.values_list('departamento', flat=True).distinct().order_by('departamento')
    # Municipios
    municipios = Tablero.objects.values_list('municipio', flat=True).distinct().order_by('municipio')
    # ESE
    ese = Tablero.objects.values_list('ese', flat=True).distinct().order_by('ese')
    # REPS códigos
    reps = Tablero.objects.values('serv_codigo', 'serv_nombre').distinct().order_by('serv_codigo')
    # Grupos códigos
    grupos = Tablero.objects.values('grse_codigo', 'grse_nombre').distinct().order_by('grse_codigo')
    # M intramural
    intramural = Tablero.objects.values_list('modalidad_intramural', flat=True).distinct().order_by('modalidad_intramural')
    # M unidad movil
    unidad_movil = Tablero.objects.values_list('modalidad_unidad_movil', flat=True).distinct().order_by('modalidad_unidad_movil')
    # M domiciliario
    domiciliario = Tablero.objects.values_list('modalidad_domiciliario', flat=True).distinct().order_by('modalidad_domiciliario')
    # M Jornada Salud
    jornada = Tablero.objects.values_list('modalidad_jornada_salud', flat=True).distinct().order_by('modalidad_jornada_salud')
    # M Telemedicina Interactiva
    interactiva = Tablero.objects.values_list('telemedicina_interactiva', flat=True).distinct().order_by('telemedicina_interactiva')
    # M Telemedicina No Interactiva
    no_interactiva = Tablero.objects.values_list('telemedicina_no_interactiva', flat=True).distinct().order_by('telemedicina_no_interactiva')
    # M Tele Experticia
    experticia = Tablero.objects.values_list('modalidad_tele_experticia', flat=True).distinct().order_by('modalidad_tele_experticia')
    # M Tele Monitoreo
    monitoreo = Tablero.objects.values_list('modalidad_tele_monitoreo', flat=True).distinct().order_by('modalidad_tele_monitoreo')

    # Datos tabla Proveedores Contratados
    proveedores = proveedores_contratados.values('nit', 'nombre', 'numero_contrato', 'year_contrato').distinct().order_by('year_contrato', 'numero_contrato','nombre')
    paginator_proveedores = Paginator(proveedores, 100)
    page_number_proveedores = request.GET.get('page')
    proveedores_page = paginator_proveedores.get_page(page_number_proveedores)

    # Datos tabla Departamentos
    departamentos = proveedores_contratados.values('departamento').distinct().order_by('departamento')

    # Datos tabla Sedes Habilitadas    
    sedes = proveedores_contratados.values('codigo_de_habilitacion', 'numero_sede', 'sede_nombre', 'departamento', 'municipio').distinct().order_by('sede_nombre')
    paginator_sedes = Paginator(sedes, 100)
    page_number_sedes = request.GET.get('page')
    sedes_page = paginator_sedes.get_page(page_number_sedes)

    # Datos tabla municipios sede
    municipios_sede = proveedores_contratados.values('municipio').distinct().order_by('municipio')

    reps_sede = proveedores_contratados.values('serv_codigo', 'serv_nombre').distinct().order_by('serv_codigo')

    grupos_sede = proveedores_contratados.values('grse_codigo', 'grse_nombre').distinct().order_by('grse_codigo')

    dpto_sedes = proveedores_contratados.values('departamento', 'municipio').distinct().order_by('departamento')

    modalidades = proveedores_contratados.values('serv_codigo', 'serv_nombre', 'modalidad_intramural', 
        'modalidad_unidad_movil', 'modalidad_domiciliario', 'modalidad_jornada_salud', 'telemedicina_interactiva', 
        'telemedicina_no_interactiva', 'modalidad_tele_experticia', 'modalidad_tele_monitoreo').distinct().order_by('modalidad_intramural')
    
    paginator_modalidades = Paginator(modalidades, 50)
    page_number_modalidades = request.GET.get('page')
    modalidades_page = paginator_modalidades.get_page(page_number_modalidades)
    
    # Datos para la torta prestadores por departamento
    prestadores_contrato = (
        proveedores_contratados.values('m_dpto')
        .annotate(total=Count('nit', distinct=True))
        .order_by('-total')
    )
    resultado = []
    for item in prestadores_contrato:
        resultado.append({
            'departamento': item['m_dpto'],
            'total': item['total']
        })
    chart_contratos = {
        'labels': [item['m_dpto'] for item in prestadores_contrato],
        'data': [item['total'] for item in prestadores_contrato],
    }    
    chart_contratos_json = json.dumps(chart_contratos)

    # Datos para la torta prestadores por departamento
    prestadores_por_depto = (
        proveedores_contratados.values('departamento')
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
        proveedores_contratados.values('departamento')
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
        proveedores_contratados.values('departamento')
        .annotate(total=Count('serv_codigo', distinct=True))
        .order_by('-total')
    )
    
    #Datos para barras por dpto
    reps_por_departamento = (
        proveedores_contratados.values('departamento', 'serv_nombre')  # Agrupar por dpto y tipo de servicio
        .annotate(total_reps=Count(Concat(F('serv_codigo'),F('codigo_de_habilitacion'),F('numero_sede')), distinct=True))
        .order_by('departamento', 'serv_nombre')  # Ordenar por dpto y servicio
    )
        # .annotate(total_reps=Count('serv_codigo'))  # Contar los REPS por cada tipo
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


    # Datos municipios por departamento dane
    dane_municipios = (
        dane.values('departamento')
        .annotate(total=Count('municipio', distinct=True))
        .order_by('-total')
    )

    # Datos para mapa municipios por departamento
    prestadores_por_municipio = (
        proveedores_contratados.values('departamento')
        .annotate(total=Count(Concat(F('departamento'),F('municipio')), distinct=True))
        .order_by('-total')
    )

    '''
    # Importo todos los arreglos del reps para comparaciones
    '''
    proveedores_reps, chart_json_reps, chart_reps_json_reps, suma_pres_dpto_reps, chart_sedes_json_reps, suma_sedes_dpto_reps, prestadores_por_depto_reps, prestadores_por_municipio_reps, sedes_por_depto_reps, reps_depto_reps, reps_sede_reps, dpto_reps, municipios_sede_reps, reps_data = repsInfo(request)

    # Datos para el mapa de calor (densidad de prestadores por departamento)
    mapa_data = list(prestadores_por_depto)
    mapa_json = json.dumps(list(mapa_data))
    # Data Mapa 2
    mapa_data_dos = mapa2(dane_dpto, dane_municipios, prestadores_por_depto, prestadores_por_municipio, sedes_por_depto, reps_depto, prestadores_por_depto_reps, prestadores_por_municipio_reps, sedes_por_depto_reps, reps_depto_reps)
    mapa_dos_json = json.dumps(mapa_data_dos)

    tablero_json = json.dumps(list(proveedores_contratados), default=str)  # Serializa a JSON


    context = {
        'tablero': tablero_json,
        'proveedores': proveedores_contratados,
        'info_page': proveedores_contratados,
        'info_reps': reps_data,
        'prov_c': proveedores,
        'positiva': proveedores_page,
        'proveedores_reps': proveedores_reps,
        'dptos': list(departamentos),
        'dptos_reps': list(dpto_reps),
        'municipios_sede': municipios_sede,
        'municipios_sede_reps': municipios_sede_reps,
        'sedes_page': sedes_page,
        'sedes_reps': suma_sedes_dpto_reps,
        'reps_sede': reps_sede,
        'reps_sede_reps': reps_sede_reps,
        'grupos_sede': grupos_sede,
        'dptos_sede': dpto_sedes,
        'modalidades_sede': modalidades_page,
        'sucursales': sucursales,
        'anos': years,
        'contratos': numero_contrato,
        'supervisores': supervisores,
        'categorias': categorias_cuentas_medicas,
        'numeros_sedes': numeros_sedes,        
        'departamentos': dptos,
        'municipios': municipios,
        'eses': ese,
        'reps': reps,
        'grupos': grupos,
        'intramural': intramural,
        'unidad_movil': unidad_movil,
        'domiciliario': domiciliario,
        'jornada': jornada,
        'interactiva': interactiva,
        'no_interactiva': no_interactiva,
        'experticia': experticia,
        'monitoreo': monitoreo,
        'chart': chart_json,
        'chart_reps': chart_reps_json,
        'chart_contratos': chart_contratos_json,
        'suma_chart': suma_pres_dpto,
        'chart_sedes': chart_sedes_json,
        'suma_chart_sedes': suma_sedes_dpto,
        'mapa': mapa_json,
        'mapa_dos': mapa_dos_json,
        'data_page': data_page,
        'filtros_aplicados': filtros_aplicados,
        'page_title': 'Tablero Red Asistencial',
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Convertir QuerySets a listas para poder serializar en JSON
            data_json = {
                'prov_c': list(proveedores),  # list(...) de diccionarios
                # 'sedes': list(sedes),
                'departamentos': list(departamentos),
                'municipios_sede': list(municipios_sede),
                'reps_sede': list(reps_sede),
                'grupos_sede': list(grupos_sede),
                'modalidades_sede': list(modalidades),
                'chart_data': chart_data,
                'chart_data_sedes': chart_data_sedes,
                'mapa_data': mapa_data,
                'mapa_data_dos': mapa_data_dos,
            }
            html = render_to_string('partials/dashboard_table.html', {'data_page': data_page})
            proveedores = render_to_string('partials/dashboard_table_proveedores.html', {'positiva': proveedores_page})
            sedes = render_to_string('partials/dashboard_table_sedes.html', {'sedes_page': sedes_page})
            modalidades = render_to_string('partials/dashboard_table_modalidades.html', {'modalidades_sede': modalidades_page})
            data_json['html'] = html
            data_json['proveedores'] = proveedores
            data_json['sedes'] = sedes
            data_json['modalidades'] = modalidades
            return JsonResponse(data_json, safe=False)

    return render(request, 'dashboard.html', context)
