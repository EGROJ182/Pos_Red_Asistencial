from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_proveedores import proveedores
from ..modules.alert import alert
from ..modules.mail import send_email
from django.http import JsonResponse
from django.template.loader import render_to_string
from collections import defaultdict
import json

# Create your views here.
def proveedoresContratados(request):
    # Consulta a Base de datos
    proveedores_contratados = proveedores.objects.all()

    # Filtrado según los parámetros del formulario
    filter_nit = request.GET.get('nit')
    filter_nombre = request.GET.get('nombre')
    filter_tipo_proveedor = request.GET.get('tipo_proveedor')
    filter_numero_contrato = request.GET.get('numero_contrato')
    filter_year_contrato = request.GET.get('year_contrato')
    filter_sucursal = request.GET.get('sucursal')
    filter_supervisor = request.GET.get('supervisor')
    filter_categoria = request.GET.get('categoria')
    filter_complejidad = request.GET.get('complejidad')
    filter_categoria_cuentas_medicas = request.GET.get('categoria_cuentas_medicas')
    filter_departamento = request.GET.get('departamento')
    filter_municipio = request.GET.get('municipio')
    filter_novedad = request.GET.get('novedad')

    filtros_aplicados = []

    if filter_nit:
        proveedores_contratados = proveedores_contratados.filter(nit__icontains=filter_nit)
        filtros_aplicados.append(f"NIT: {filter_nit}")
    if filter_nombre:
        proveedores_contratados = proveedores_contratados.filter(nombre__icontains=filter_nombre)
        filtros_aplicados.append(f"Nombre Proveedor: {filter_nombre}")
    if filter_tipo_proveedor:
        proveedores_contratados = proveedores_contratados.filter(tipo_proveedor=filter_tipo_proveedor)
        filtros_aplicados.append(f"Tipo de Proveedor: {filter_tipo_proveedor}")
    if filter_numero_contrato:
        proveedores_contratados = proveedores_contratados.filter(numero_contrato=filter_numero_contrato)
        filtros_aplicados.append(f"Número de Contrato: {filter_numero_contrato}")
    if filter_year_contrato:
        proveedores_contratados = proveedores_contratados.filter(year_contrato=filter_year_contrato)
        filtros_aplicados.append(f"Año Contrato: {filter_year_contrato}")
    if filter_sucursal:
        proveedores_contratados = proveedores_contratados.filter(sucursal=filter_sucursal)
        filtros_aplicados.append(f"Sucursal: {filter_sucursal}")
    if filter_supervisor:
        proveedores_contratados = proveedores_contratados.filter(supervisor=filter_supervisor)
        filtros_aplicados.append(f"Supervisor: {filter_supervisor}")
    if filter_categoria:
        proveedores_contratados = proveedores_contratados.filter(categoria=filter_categoria)
        filtros_aplicados.append(f"Categoría: {filter_categoria}")
    if filter_complejidad:
        proveedores_contratados = proveedores_contratados.filter(complejidad=filter_complejidad)
        filtros_aplicados.append(f"Complejidad: {filter_complejidad}")
    if filter_categoria_cuentas_medicas:
        proveedores_contratados = proveedores_contratados.filter(categoria_cuentas_medicas=filter_categoria_cuentas_medicas)
        filtros_aplicados.append(f"Categoría Cuentas Médicas: {filter_categoria_cuentas_medicas}")
    if filter_departamento:
        proveedores_contratados = proveedores_contratados.filter(departamento=filter_departamento)
        filtros_aplicados.append(f"Departamento: {filter_departamento}")
    if filter_municipio:
        proveedores_contratados = proveedores_contratados.filter(municipio=filter_municipio)
        filtros_aplicados.append(f"Municipio: {filter_municipio}")
    if filter_novedad:
        proveedores_contratados = proveedores_contratados.filter(novedad=filter_novedad)
        filtros_aplicados.append(f"Novedad en Maestra: {filter_novedad}")

    paginator = Paginator(proveedores_contratados, 20)
    page_number = request.GET.get('page')
    proveedores_page = paginator.get_page(page_number)

    # Tipos
    tipos = proveedores.objects.values_list('tipo_proveedor', flat=True).distinct().order_by('tipo_proveedor')
    # Sucursales
    sucursales = proveedores.objects.values_list('sucursal', flat=True).distinct().order_by('sucursal')
    # Años
    years = proveedores.objects.values_list('year_contrato', flat=True).distinct().order_by('year_contrato')
    # Números Contratos
    numero_contrato = proveedores.objects.values_list('numero_contrato', flat=True).distinct().order_by('numero_contrato')
    # Supervisores
    supervisores = proveedores.objects.values_list('supervisor', flat=True).distinct().order_by('supervisor')
    # Categorias
    categorias = proveedores.objects.values_list('categoria', flat=True).distinct().order_by('categoria')
    # Complejidades
    complejidades = proveedores.objects.values_list('complejidad', flat=True).distinct().order_by('complejidad')
    # Categorias Cuentas Médicas
    categorias_cuentas_medicas = proveedores.objects.values_list('categoria_cuentas_medicas', flat=True).distinct().order_by('categoria_cuentas_medicas')
    # Departamentos
    dptos = proveedores.objects.values_list('departamento', flat=True).distinct().order_by('departamento')
    # Municipios
    municipios = proveedores.objects.values_list('municipio', flat=True).distinct().order_by('municipio')
    # Novedades
    novedades = proveedores.objects.values_list('novedad', flat=True).distinct().order_by('novedad')


    pts = proveedores.objects.filter(tipo_proveedor="PRESTADOR DE TECNOLOGÍAS DE SALUD")
    pss = proveedores.objects.filter(tipo_proveedor="PRESTADOR DE SERVICIOS DE SALUD")
    otros = proveedores.objects.filter(tipo_proveedor="otro")

    # Generación de mapa_data dinámico
    mapa_data = []
    departamentos = proveedores_contratados.values('departamento', 'latitud', 'longitud').distinct()

    for dep in departamentos:
        proveedores_departamento = proveedores_contratados.filter(departamento=dep['departamento'])
        proveedores_info = []
        
        for proveedor in proveedores_departamento:
            proveedores_info.append({
                'nombre': proveedor.nombre,
                'direccion': proveedor.direccion,
                'tipo_proveedor': proveedor.tipo_proveedor,
            })

        mapa_data.append({
            'departamento': dep['departamento'],
            'lat': float(dep['latitud']),
            'lng': float(dep['longitud']),
            'proveedores': proveedores_info
        })

    # print(json.dumps(mapa_data))
    if filter_nombre == 'enviar correo':
        send_email()

    vencidos = [alert for alert in alert(proveedores) if alert.dias_restantes < 0]
    cero = [alert for alert in alert(proveedores) if alert.dias_restantes == 0]
    uno = [alert for alert in alert(proveedores) if alert.dias_restantes == 1]
    dos = [alert for alert in alert(proveedores) if alert.dias_restantes == 2]
    tres = [alert for alert in alert(proveedores) if alert.dias_restantes > 2 and alert.dias_restantes < 8]
    cuatro = [alert for alert in alert(proveedores) if alert.dias_restantes > 7 and alert.dias_restantes < 16]
    cinco = [alert for alert in alert(proveedores) if alert.dias_restantes > 15]

    context = {
        'proveedores': proveedores_page,
        'info_page': proveedores_page,
        'proveedores_mapa': proveedores_contratados,
        'tipos': tipos,
        'sucursales': sucursales,
        'years': years,
        'numero_contrato': numero_contrato,
        'supervisores': supervisores,
        'categorias': categorias,
        'categorias_cuentas_medicas': categorias_cuentas_medicas,
        'complejidades': complejidades,
        'departamentos': dptos,
        'municipios': municipios,
        'novedades': novedades,
        'pts': pts,
        'pss': pss,
        'otros': otros,
        'vencidos': vencidos,
        'cero': cero,
        'uno': uno,
        'dos': dos,
        'tres': tres,
        'cuatro': cuatro,
        'cinco': cinco,
        'filtros_aplicados': filtros_aplicados,
        'mapa_data': mapa_data,
        'alerts': alert(proveedores),
        'page_title': 'Proveedores'
    }
    
    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/proveedores_table.html', {'proveedores': proveedores_page})
        return JsonResponse({'html': html})

    return render(request, 'proveedores.html', context)
