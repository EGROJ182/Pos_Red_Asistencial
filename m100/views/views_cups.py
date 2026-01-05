from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_cups import Cups
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def cups(request):
    # Consulta a Base de datos
    cups = Cups.objects.using('dataTarifas').all()

    # Filtrado según los parámetros del formulario
    filter_cups = request.GET.get('codigo_cups')
    filter_descripcion = request.GET.get('descripcion_del_cups')
    filter_nombre = request.GET.get('nombre')
    filter_nit = request.GET.get('nit')
    filter_departamento = request.GET.get('departamento')
    filter_municipio = request.GET.get('municipio')

    filtros_aplicados = []

    if filter_cups:
        cups = cups.filter(codigo_cups__icontains=filter_cups)
        filtros_aplicados.append(f"Codigo CUPS: {filter_cups}")
    if filter_descripcion:
        cups = cups.filter(descripcion_del_cups__icontains=filter_descripcion)
        filtros_aplicados.append(f"Descripción: {filter_descripcion}")
    if filter_nombre:
        cups = cups.filter(nombre=filter_nombre)
        filtros_aplicados.append(f"Prestador: {filter_nombre}")
    if filter_nit:
        cups = cups.filter(nit__icontains=filter_nit)
        filtros_aplicados.append(f"NIT: {filter_nit}")
    if filter_departamento:
        cups = cups.filter(departamento=filter_departamento)
        filtros_aplicados.append(f"Departamento: {filter_departamento}")
    if filter_municipio:
        cups = cups.filter(municipio=filter_municipio)
        filtros_aplicados.append(f"Municipio: {filter_municipio}")


    paginator = Paginator(cups, 20)
    page_number = request.GET.get('page')
    cups_page = paginator.get_page(page_number)
    
    # Prestadores Contratados únicas
    prestadores = Cups.objects.using('dataTarifas').values_list('nombre', flat=True).distinct().order_by('nombre')
    # Departamentos únicas
    departamentos = Cups.objects.using('dataTarifas').values_list('departamento', flat=True).distinct().order_by('departamento')
    # Municipios únicas
    municipios = Cups.objects.using('dataTarifas').values_list('municipio', flat=True).distinct().order_by('municipio')

    context = {
        'cups': cups_page,
        'info_page': cups_page,
        'prestadores': prestadores,
        'departamentos': departamentos,
        'municipios': municipios,
        'filtros_aplicados': filtros_aplicados,
        'page_title': 'CUPS'
    }

    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/cups_table.html', {'cups': cups_page})
        return JsonResponse({'html': html})

    return render(request, 'cups.html', context)