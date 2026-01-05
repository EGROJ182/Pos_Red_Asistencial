from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_termometro import termometro
from ..modules.color_cell_alert import alert_color_termometro
from ..models.models_proveedores import proveedores
from ..modules.alert import alert
# from ..modules.info_actas import info_actas, total_actas
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def expTermometro(request):
    # Consulta a Base de datos
    expedientes = termometro.objects.all()

    # Filtrado según los parámetros del formulario
    filter_expediente = request.GET.get('expediente_invima')
    filter_principio_activo = request.GET.get('principio_activo')
    filter_concentracion = request.GET.get('concentracion')
    filter_unidad_de_dispensacion = request.GET.get('unidad_de_dispensacion')
    filter_nombre_comercial = request.GET.get('nombre_comercial')
    filter_fabricante = request.GET.get('fabricante')
    filter_medicamento = request.GET.get('medicamento')
    filter_canal = request.GET.get('canal')
    filter_factores_precio = request.GET.get('factores_precio')

    cantidad = request.GET.get('cantidad')

    filtros_aplicados = []

    if filter_expediente:
        expedientes = expedientes.filter(expediente_invima__icontains=filter_expediente)
        filtros_aplicados.append(f"Expediente: {filter_expediente}")
    if filter_principio_activo:
        expedientes = expedientes.filter(principio_activo__icontains=filter_principio_activo)
        filtros_aplicados.append(f"Principio Activo: {filter_principio_activo}")
    if filter_concentracion:
        expedientes = expedientes.filter(concentracion__icontains=filter_concentracion)
        filtros_aplicados.append(f"Concentración: {filter_concentracion}")
    if filter_unidad_de_dispensacion:
        expedientes = expedientes.filter(unidad_de_dispensacion=filter_unidad_de_dispensacion)
        filtros_aplicados.append(f"Unidad de Dispensación: {filter_unidad_de_dispensacion}")
    if filter_nombre_comercial:
        expedientes = expedientes.filter(nombre_comercial__icontains=filter_nombre_comercial)
        filtros_aplicados.append(f"Nombre Comercial: {filter_nombre_comercial}")
    if filter_fabricante:
        expedientes = expedientes.filter(fabricante__icontains=filter_fabricante)
        filtros_aplicados.append(f"Fabricante: {filter_fabricante}")
    if filter_medicamento:
        expedientes = expedientes.filter(medicamento__icontains=filter_medicamento)
        filtros_aplicados.append(f"Medicamento: {filter_medicamento}")
    if filter_canal:
        expedientes = expedientes.filter(canal=filter_canal)
        filtros_aplicados.append(f"Canal: {filter_canal}")
    if filter_factores_precio:
        expedientes = expedientes.filter(factores_precio=filter_factores_precio)
        filtros_aplicados.append(f"Factores Precio: {filter_factores_precio}")

    paginator = Paginator(expedientes, 20)
    page_number = request.GET.get('page')
    expedientes_page = paginator.get_page(page_number)

    cantidad = cantidad if cantidad and cantidad.isnumeric() else 1

    # Creo un diccionario con los expedientes y sus propiedades para mi vista
    expedientes_color = [
        {
            'expediente': expediente,
            'color': alert_color_termometro(expediente.factores_precio),
            'cantidad': cantidad,
            'total': float(cantidad)*float(expediente.precio_por_tableta),
            'precio_con_porcentaje': float(expediente.precio_por_tableta)*1.12
        }
        for expediente in expedientes_page
    ]
    
    # Unidades Base únicas
    unidades_base = termometro.objects.values_list('unidad_base', flat=True).distinct().order_by('unidad_base')
    # Unidades de Dispensación únicas
    unidades_de_dispensacion = termometro.objects.values_list('unidad_de_dispensacion', flat=True).distinct().order_by('unidad_de_dispensacion')
    # Fabricantes únicos
    fabricantes = termometro.objects.values_list('fabricante', flat=True).distinct().order_by('fabricante')
    # Canales únicas
    canales = termometro.objects.values_list('canal', flat=True).distinct().order_by('canal')
    # Factores Precio únicos
    factores_precio = termometro.objects.values_list('factores_precio', flat=True).distinct().order_by('factores_precio')

    # Importo la Consulta a Base de datos Total Actas para mostrarla en la vista
    # total_actas_medicamentos = total_actas(m100)
    
    context = {
        'expedientes': expedientes_color,
        'info_page' : expedientes_page,
        'unidades_base': unidades_base,
        'unidades_de_dispensacion': unidades_de_dispensacion,
        'fabricantes': fabricantes,
        'canales': canales,
        'factores_precio': factores_precio,
        'filtros_aplicados': filtros_aplicados,
        'cantidad': cantidad,
        'alerts': alert(proveedores),
        'vencidos': [alert for alert in alert(proveedores) if alert.dias_restantes < 0],
        'cero': [alert for alert in alert(proveedores) if alert.dias_restantes == 0],
        'uno': [alert for alert in alert(proveedores) if alert.dias_restantes == 1],
        'dos': [alert for alert in alert(proveedores) if alert.dias_restantes == 2],
        'tres': [alert for alert in alert(proveedores) if alert.dias_restantes > 2 and alert.dias_restantes < 8],
        'cuatro': [alert for alert in alert(proveedores) if alert.dias_restantes > 7 and alert.dias_restantes < 16],
        'cinco': [alert for alert in alert(proveedores) if alert.dias_restantes > 15],
        'page_title': 'Termómetro'
    }
    
    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/termometro_table.html', {'expedientes': expedientes_color})
        return JsonResponse({'html': html})

    return render(request, 'termometro.html', context)
