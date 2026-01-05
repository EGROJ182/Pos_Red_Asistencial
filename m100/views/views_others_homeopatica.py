from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_others_homeopatica import Othersfh as Others
from ..models.models_med_homeopatica import m100fh as m100
from ..modules.color_cell_alert import alert_color
from ..modules.info_actas import info_actas_medicamentos_fh, info_actas_otros_fh
from ..modules.estandar import obtener_datos_estandar_fh, total_estandar
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def othersHomeopatica(request):
    # Consulta a Base de datos
    others = Others.objects.all().order_by('-fecha_pactada')

    # Filtrado según los parámetros del formulario
    filter_cum = request.GET.get('cum')
    filter_expediente = request.GET.get('expediente')
    filter_descripcion = request.GET.get('descripcion_medicamento')
    filter_principio_activo = request.GET.get('principio_activo')
    filter_concentracion = request.GET.get('concentracion')
    filter_nit = request.GET.get('nit_proveedor')
    filter_forma_farmaceutica = request.GET.get('forma_farmaceutica')
    filter_alianza = request.GET.get('alianza')
    filter_canal = request.GET.get('canal')
    filter_acta = request.GET.get('numero_acta_inicial')
    filter_proveedor = request.GET.get('nombre_del_proveedor_pactado')
    filter_tipo = request.GET.get('tipo')
    filter_novedad = request.GET.get('novedad')

    filtros_aplicados = []

    if filter_cum:
        others = others.filter(cum__icontains=filter_cum)
        filtros_aplicados.append(f"CUM: {filter_cum}")
    if filter_expediente:
        others = others.filter(expediente__icontains=filter_expediente)
        filtros_aplicados.append(f"Expediente: {filter_expediente}")
    if filter_descripcion:
        others = others.filter(descripcion_medicamento__icontains=filter_descripcion)
        filtros_aplicados.append(f"Descripción Insumo : {filter_descripcion}")
    if filter_principio_activo:
        others = others.filter(principio_activo__icontains=filter_principio_activo)
        filtros_aplicados.append(f"Principio Activo: {filter_principio_activo}")
    if filter_concentracion:
        others = others.filter(concentracion__icontains=filter_concentracion)
        filtros_aplicados.append(f"Concentración: {filter_concentracion}")
    if filter_nit:
        others = others.filter(nit_proveedor__icontains=filter_nit)
        filtros_aplicados.append(f"NIT: {filter_nit}")
    if filter_forma_farmaceutica:
        others = others.filter(forma_farmaceutica=filter_forma_farmaceutica)
        filtros_aplicados.append(f"Forma Farmacéutica: {filter_forma_farmaceutica}")
    if filter_alianza:
        others = others.filter(alianza=filter_alianza)
        filtros_aplicados.append(f"Alianza: {filter_alianza}")
    if filter_canal:
        others = others.filter(canal=filter_canal)
        filtros_aplicados.append(f"Canal: {filter_canal}")
    if filter_acta:
        others = others.filter(numero_acta_inicial=filter_acta)
        filtros_aplicados.append(f"#Acta o Estandar: {filter_acta}")
    if filter_proveedor:
        others = others.filter(nombre_del_proveedor_pactado=filter_proveedor)
        filtros_aplicados.append(f"Proveedor: {filter_proveedor}")
    if filter_tipo:
        others = others.filter(tipo=filter_tipo)
        filtros_aplicados.append(f"Tipo: {filter_tipo}")
    if filter_novedad:
        others = others.filter(novedad=filter_novedad)
        filtros_aplicados.append(f"Novedad: {filter_novedad}")

    paginator = Paginator(others, 20)
    page_number = request.GET.get('page')
    others_page = paginator.get_page(page_number)
    
    # Creo un diccionario con los insumos y sus propiedades para mi vista
    others_color = [
        {
            'other': other,
            'color': alert_color(other.novedad)
        }
        for other in others_page
    ]

    # Formas farmacéuticas únicas
    formas_farmaceuticas = Others.objects.values_list('forma_farmaceutica', flat=True).distinct().order_by('forma_farmaceutica')
    # Alianzas únicas
    alianza = Others.objects.values_list('alianza', flat=True).distinct().order_by('alianza')
    # Canal únicas
    canal = Others.objects.values_list('canal', flat=True).distinct().order_by('canal')
    # Numero Acta Inicial únicas
    acta = Others.objects.values_list('numero_acta_inicial', flat=True).distinct().order_by('numero_acta_inicial')
    # Proveedores únicas
    proveedores = Others.objects.values_list('nombre_del_proveedor_pactado', flat=True).distinct().order_by('nombre_del_proveedor_pactado')
    # Tipos únicas
    tipos = Others.objects.values_list('tipo', flat=True).distinct().order_by('tipo')
    # Novedades únicas
    novedades = Others.objects.values_list('novedad', flat=True).distinct().order_by('novedad')

    # Importo la Consulta a Base de datos Total Actas para mostrarla en la vista
    # total_actas_others = total_actas(Others)

    context = {
        'others': others_color,
        'info_page': others_page,
        'info_actas_m100': info_actas_medicamentos_fh(m100),
        'info_actas_otros' : info_actas_otros_fh(Others),
        'formas_farmaceuticas': formas_farmaceuticas,
        'alianza': alianza,
        'canal': canal,
        'acta': acta,
        'proveedores': proveedores,
        'tipos': tipos,
        'novedades': novedades,
        'filtros_aplicados': filtros_aplicados,
        'estandar' : obtener_datos_estandar_fh(m100, Others),
        'tarifario' : total_estandar(m100, Others),
        'page_title': 'HC Otros'
    }

    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/others_table.html', {'others': others_color})
        return JsonResponse({'html': html})

    return render(request, 'others_homeopatica.html', context)
