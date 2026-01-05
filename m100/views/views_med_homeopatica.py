from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_med_homeopatica import m100fh as m100
from ..models.models_others_homeopatica import Othersfh as otros
from ..modules.color_cell_alert import alert_color
from ..modules.info_actas import info_actas_medicamentos_fh, info_actas_otros_fh
from ..modules.estandar import obtener_datos_estandar_fh, total_estandar
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def medicamentosHomeopatica(request):
    # Consulta a Base de datos
    medicamentos = m100.objects.all().order_by('-fecha_pactada')

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
    filter_regulado = request.GET.get('valor_medicamento_regulado')
    filter_control = request.GET.get('medicamentos_de_control_especial')
    filter_monopolio = request.GET.get('medicamentos_monopolio_del_estado')
    filter_acta = request.GET.get('numero_acta_inicial')
    filter_proveedor = request.GET.get('nombre_del_proveedor_pactado')
    filter_tipo = request.GET.get('tipo')
    filter_novedad = request.GET.get('novedad')

    filtros_aplicados = []

    if filter_cum:
        medicamentos = medicamentos.filter(cum__icontains=filter_cum)
        filtros_aplicados.append(f"CUM: {filter_cum}")
    if filter_expediente:
        medicamentos = medicamentos.filter(expediente__icontains=filter_expediente)
        filtros_aplicados.append(f"Expediente: {filter_expediente}")
    if filter_descripcion:
        medicamentos = medicamentos.filter(descripcion_medicamento__icontains=filter_descripcion)
        filtros_aplicados.append(f"Descripción MED: {filter_descripcion}")
    if filter_principio_activo:
        medicamentos = medicamentos.filter(principio_activo__icontains=filter_principio_activo)
        filtros_aplicados.append(f"Principio Activo: {filter_principio_activo}")
    if filter_concentracion:
        medicamentos = medicamentos.filter(concentracion__icontains=filter_concentracion)
        filtros_aplicados.append(f"Concentración: {filter_concentracion}")
    if filter_nit:
        medicamentos = medicamentos.filter(nit_proveedor__icontains=filter_nit)
        filtros_aplicados.append(f"NIT: {filter_nit}")
    if filter_forma_farmaceutica:
        medicamentos = medicamentos.filter(forma_farmaceutica=filter_forma_farmaceutica)
        filtros_aplicados.append(f"Forma Farmacéutica: {filter_forma_farmaceutica}")
    if filter_alianza:
        medicamentos = medicamentos.filter(alianza=filter_alianza)
        filtros_aplicados.append(f"Alianza: {filter_alianza}")
    if filter_canal:
        medicamentos = medicamentos.filter(canal=filter_canal)
        filtros_aplicados.append(f"Canal: {filter_canal}")
    if filter_control:
        medicamentos = medicamentos.filter(medicamentos_de_control_especial=filter_control)
        filtros_aplicados.append(f"Control Especial: {filter_control}")
    if filter_monopolio:
        medicamentos = medicamentos.filter(medicamentos_monopolio_del_estado=filter_monopolio)
        filtros_aplicados.append(f"Monopolio: {filter_monopolio}")
    if filter_acta:
        medicamentos = medicamentos.filter(numero_acta_inicial=filter_acta)
        filtros_aplicados.append(f"#Acta o Estandar: {filter_acta}")
    if filter_proveedor:
        medicamentos = medicamentos.filter(nombre_del_proveedor_pactado=filter_proveedor)
        filtros_aplicados.append(f"Proveedor: {filter_proveedor}")
    if filter_tipo:
        medicamentos = medicamentos.filter(tipo=filter_tipo)
        filtros_aplicados.append(f"Tipo: {filter_tipo}")
    if filter_novedad:
        medicamentos = medicamentos.filter(novedad=filter_novedad)
        filtros_aplicados.append(f"Novedad: {filter_novedad}")

    # Regulados
    if filter_regulado:    
        filtros_aplicados.append(f"Regulado: {filter_regulado}")
        if filter_regulado.lower() == 'si':
            medicamentos = medicamentos.filter(valor_medicamento_regulado__gt=0)  # Mayor que 0
        elif filter_regulado.lower() == 'no':
            medicamentos = medicamentos.filter(_medicamento_regulado=0)  # Igual a 0

    paginator = Paginator(medicamentos, 20)
    page_number = request.GET.get('page')
    medicamentos_page = paginator.get_page(page_number)

    # Creo un diccionario con los medicamentos y sus propiedades para mi vista
    medicamentos_color = [
        {
            'medicamento': medicamento,
            'color': alert_color(medicamento.novedad)
        }
        for medicamento in medicamentos_page
    ]
    
    # Formas farmacéuticas únicas
    formas_farmaceuticas = m100.objects.values_list('forma_farmaceutica', flat=True).distinct().order_by('forma_farmaceutica')
    # Alianzas únicas
    alianza = m100.objects.values_list('alianza', flat=True).distinct().order_by('alianza')
    # Canal únicas
    canal = m100.objects.values_list('canal', flat=True).distinct().order_by('canal')
    # Control Especial únicas
    control = m100.objects.values_list('medicamentos_de_control_especial', flat=True).distinct().order_by('medicamentos_de_control_especial')
    # Monopolio del Estado únicas
    monopolio = m100.objects.values_list('medicamentos_monopolio_del_estado', flat=True).distinct().order_by('medicamentos_monopolio_del_estado')
    # Numero Acta Inicial únicas
    acta = m100.objects.values_list('numero_acta_inicial', flat=True).distinct().order_by('numero_acta_inicial')
    # Proveedores únicas
    proveedores = m100.objects.values_list('nombre_del_proveedor_pactado', flat=True).distinct().order_by('nombre_del_proveedor_pactado')
    # Tipos únicas
    tipos = m100.objects.values_list('tipo', flat=True).distinct().order_by('tipo')
    # Novedades únicas
    novedades = m100.objects.values_list('novedad', flat=True).distinct().order_by('novedad')

    # Importo la Consulta a Base de datos Total Actas para mostrarla en la vista
    # total_actas_medicamentos = total_actas(m100)
    
    # Proveedores consulta
    proveedores_consulta = medicamentos_page
    
    context = {
        'medicamentos': medicamentos_color,
        'info_page' : medicamentos_page,
        'info_actas_m100' : info_actas_medicamentos_fh(m100),
        'info_actas_otros' : info_actas_otros_fh(otros),
        'formas_farmaceuticas': formas_farmaceuticas,
        'alianza': alianza,
        'canal': canal,
        'control_especial': control,
        'monopolio': monopolio,
        'acta': acta,
        'proveedores': proveedores,
        'proveedores_consulta': proveedores_consulta,
        'tipos': tipos,
        'novedades': novedades,
        'filtros_aplicados': filtros_aplicados,
        'estandar' : obtener_datos_estandar_fh(m100, otros),
        'tarifario' : total_estandar(m100, otros),
        'page_title': 'Historico de Medicamentos (Farmacia Homeopatica)'
    }
    
    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/medicamentos_table.html', {'medicamentos': medicamentos_color})
        return JsonResponse({'html': html})

    return render(request, 'medicamentos_homeopatica.html', context)
