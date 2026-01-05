from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_med_ce import MCE as med_control_especial
from ..modules.color_cell_alert import alert_color
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def MCE(request):
    # Consulta a Base de datos
    mce = med_control_especial.objects.all()

    # Filtrado según los parámetros del formulario
    filter_dci = request.GET.get('dci')
    filter_dci_busqueda = request.GET.get('dci_busqueda')
    filter_concentracion = request.GET.get('concentracion')
    filter_forma_farmaceutica = request.GET.get('forma_farmaceutica')
    filter_nota = request.GET.get('nota')
    filter_cum = request.GET.get('codigo_cum')

    filtros_aplicados = []

    if filter_dci:
        mce = mce.filter(dci__icontains=filter_dci)
        filtros_aplicados.append(f"Denominación Común Internacional (DCI): {filter_cum}")
    if filter_dci_busqueda:
        mce = mce.filter(dci_busqueda__icontains=filter_dci_busqueda)
        filtros_aplicados.append(f"(DCI) Búsqueda): {filter_dci_busqueda}")
    if filter_concentracion:
        mce = mce.filter(concentracion__icontains=filter_concentracion)
        filtros_aplicados.append(f"Concentración: {filter_concentracion}")
    if filter_forma_farmaceutica:
        mce = mce.filter(forma_farmaceutica=filter_forma_farmaceutica)
        filtros_aplicados.append(f"Forma Farmacéutica: {filter_forma_farmaceutica}")
    if filter_nota:
        mce = mce.filter(nota=filter_nota)
        filtros_aplicados.append(f"Nota: {filter_nota}")
    if filter_cum:
        mce = mce.filter(codigo_cum__icontains=filter_cum)
        filtros_aplicados.append(f"Código CUM: {filter_cum}")


    paginator = Paginator(mce, 20)
    page_number = request.GET.get('page')
    mce_page = paginator.get_page(page_number)

    
    # Formas farmacéuticas únicas
    formas_farmaceuticas = med_control_especial.objects.values_list('forma_farmaceutica', flat=True).distinct().order_by('forma_farmaceutica')
    # Notas
    notas = med_control_especial.objects.values_list('nota', flat=True).distinct().order_by('nota')

    context = {
        'mce': mce_page,
        'info_page' : mce_page,
        'formas_farmaceuticas': formas_farmaceuticas,
        'notas': notas,
        'filtros_aplicados': filtros_aplicados,
        'page_title': 'Controlados'
    }
    
    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/med_controlados_table.html', {'mce': mce_page})
        return JsonResponse({'html': html})

    return render(request, 'med_controlados.html', context)
