from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_datos_proveedores import infoProveedores
from django.http import JsonResponse
from django.template.loader import render_to_string
from collections import defaultdict
import json

# Create your views here.
def datosProveedores(request):
    # Consulta a Base de datos
    datos_proveedores = infoProveedores.objects.all()

    # Filtrado según los parámetros del formulario
    filter_nit = request.GET.get('nit')
    filter_name = request.GET.get('name')
    filter_departament = request.GET.get('departament')
    filter_city = request.GET.get('city')
    filter_phone = request.GET.get('phone')
    filter_cell = request.GET.get('cell')

    filtros_aplicados = []

    if filter_nit:
        datos_proveedores = datos_proveedores.filter(nit__icontains=filter_nit)
        filtros_aplicados.append(f"NIT: {filter_nit}")
    if filter_name:
        datos_proveedores = datos_proveedores.filter(name__icontains=filter_name)
        filtros_aplicados.append(f"Razón Social: {filter_name}")
    if filter_departament:
        datos_proveedores = datos_proveedores.filter(departament=filter_departament)
        filtros_aplicados.append(f"Departamento: {filter_departament}")
    if filter_city:
        datos_proveedores = datos_proveedores.filter(city=filter_city)
        filtros_aplicados.append(f"Municipio: {filter_city}")
    if filter_phone:
        datos_proveedores = datos_proveedores.filter(phone__icontains=filter_phone)
        filtros_aplicados.append(f"Teléfono: {filter_phone}")
    if filter_cell:
        datos_proveedores = datos_proveedores.filter(cell__icontains=filter_cell)
        filtros_aplicados.append(f"Celular: {filter_cell}")

    paginator = Paginator(datos_proveedores, 20)
    page_number = request.GET.get('page')
    proveedores_page = paginator.get_page(page_number)

    # Departamentos
    dptos = infoProveedores.objects.values_list('departament', flat=True).distinct().order_by('departament')
    # Municipios
    municipios = infoProveedores.objects.values_list('city', flat=True).distinct().order_by('city')
    
    # Generación de mapa_data dinámico
    # mapa_data = []
    # departamentos = datos_proveedores.values('departamento', 'latitud', 'longitud').distinct()

    # for dep in departamentos:
    #     proveedores_departamento = datos_proveedores.filter(departamento=dep['departamento'])
    #     proveedores_info = []
        
    #     for proveedor in proveedores_departamento:
    #         proveedores_info.append({
    #             'nombre': proveedor.nombre,
    #             'direccion': proveedor.direccion,
    #             'tipo_proveedor': proveedor.tipo_proveedor,
    #         })

    #     mapa_data.append({
    #         'departamento': dep['departamento'],
    #         'lat': float(dep['latitud']),
    #         'lng': float(dep['longitud']),
    #         'proveedores': proveedores_info
    #     })

    # print(json.dumps(mapa_data))

    context = {
        'proveedores': proveedores_page,
        'info_page': proveedores_page,
        'proveedores_mapa': datos_proveedores,
        'departamentos': dptos,
        'municipios': municipios,
        # 'pts': pts,
        # 'pss': pss,
        # 'otros': otros,
        'filtros_aplicados': filtros_aplicados,
        # 'mapa_data': mapa_data,
        'page_title': 'Proveedores'
    }
    
    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/datos_proveedores_table.html', {'proveedores': proveedores_page})
        return JsonResponse({'html': html})

    return render(request, 'datos_contacto_proveedores.html', context)
