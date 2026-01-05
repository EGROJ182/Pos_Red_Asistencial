from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_dane import dane_data
from ..modules.color_cell_alert import alert_img_zona, alert_color_zona
# from ..modules.info_actas import info_actas, total_actas
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def data_dane(request):
    # Consulta a Base de datos
    dane = dane_data.objects.all()

    # Filtrado según los parámetros del formulario
    filter_region = request.GET.get('region')
    filter_codigo_dpto = request.GET.get('codigo_del_departamento')
    filter_departamento = request.GET.get('departamento')
    filter_codigo_municipio = request.GET.get('codigo_del_municipio')
    filter_municipio = request.GET.get('municipio')
    filter_codigo_dane = request.GET.get('codigo_dane')
    filter_zona_especial = request.GET.get('zona_especial')

    filtros_aplicados = []

    if filter_region:
        dane = dane.filter(region=filter_region)
        filtros_aplicados.append(f"Región: {filter_region}")
    if filter_codigo_dpto:
        dane = dane.filter(codigo_del_departamento=filter_codigo_dpto)
        filtros_aplicados.append(f"Código Departamento: {filter_codigo_dpto}")
    if filter_departamento:
        dane = dane.filter(departamento=filter_departamento)
        filtros_aplicados.append(f"Departamento: {filter_departamento}")
    if filter_codigo_municipio:
        dane = dane.filter(codigo_del_municipio=filter_codigo_municipio)
        filtros_aplicados.append(f"Código Municipio: {filter_codigo_municipio}")
    if filter_municipio:
        dane = dane.filter(municipio=filter_municipio)
        filtros_aplicados.append(f"Municipio: {filter_municipio}")
    if filter_codigo_dane:
        dane = dane.filter(codigo_dane=filter_codigo_dane)
        filtros_aplicados.append(f"Código DANE: {filter_codigo_dane}")
    if filter_zona_especial:
        dane = dane.filter(zona_especial=filter_zona_especial)
        filtros_aplicados.append(f"Zona Especial: {filter_zona_especial}")

    paginator = Paginator(dane, 20)
    page_number = request.GET.get('page')
    dane_page = paginator.get_page(page_number)

    # Creo un diccionario con los expedientes y sus propiedades para mi vista
    dane_color = [
        {
            'dane': dane,
            'color': alert_color_zona(dane.zona_especial),
            'img': alert_img_zona(dane.zona_especial)
        }
        for dane in dane_page
    ]
    
    # Regiones únicas
    regiones = dane_data.objects.values_list('region', flat=True).distinct().order_by('region')
    # Codigos de los DPTO únicas
    codigos_dpto = dane_data.objects.values_list('codigo_del_departamento', flat=True).distinct().order_by('codigo_del_departamento')
    # Departamentos únicos
    departamentos = dane_data.objects.values_list('departamento', flat=True).distinct().order_by('departamento')
    # Codigos de los Municipios únicas
    codigos_municipio = dane_data.objects.values_list('codigo_del_municipio', flat=True).distinct().order_by('codigo_del_municipio')
    # Municipios únicos
    municipios = dane_data.objects.values_list('municipio', flat=True).distinct().order_by('municipio')
    # Codigos DANE únicos
    codigos_dane = dane_data.objects.values('codigo_dane', 'municipio', 'departamento').distinct().order_by('codigo_dane')
    # codigos_dane = dane_data.objects.values_list('codigo_dane', flat=True).distinct().order_by('codigo_dane')
    # Zonas Especiales únicos
    zonas_especiales = dane_data.objects.values_list('zona_especial', flat=True).distinct().order_by('zona_especial')

    # Importo la Consulta a Base de datos Total Actas para mostrarla en la vista
    # total_actas_medicamentos = total_actas(m100)

    context = {
        'dane': dane_color,
        'info_page' : dane_page,
        'regiones': regiones,
        'codigos_dpto': codigos_dpto,
        'departamentos': departamentos,
        'codigos_municipio': codigos_municipio,
        'municipios': municipios,
        'codigos_dane': codigos_dane,
        'zonas_especiales': zonas_especiales,
        'filtros_aplicados': filtros_aplicados,
        'page_title': 'DANE'
    }
    
    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/dane_table.html', {'dane': dane_color})
        return JsonResponse({'html': html})

    return render(request, 'dane.html', context)
