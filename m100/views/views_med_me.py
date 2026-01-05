from django.core.paginator import Paginator
from django.shortcuts import render
from ..models.models_med_me import MME as med_monopolio_estado
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def MME(request):
    # Consulta a Base de datos
    mme = med_monopolio_estado.objects.all()

    # Filtrado según los parámetros del formulario
    filter_dci = request.GET.get('dci')
    filter_dci_busqueda = request.GET.get('dci_busqueda')
    filter_concentracion = request.GET.get('concentracion')
    filter_forma_farmaceutica = request.GET.get('forma_farmaceutica')
    filter_nota = request.GET.get('nota')
    filter_cum = request.GET.get('codigo_cum')

    filtros_aplicados = []

    if filter_dci:
        mme = mme.filter(dci__icontains=filter_dci)
        filtros_aplicados.append(f"Denominación Común Internacional (DCI): {filter_cum}")
    if filter_dci_busqueda:
        mme = mme.filter(dci_busqueda__icontains=filter_dci_busqueda)
        filtros_aplicados.append(f"(DCI) Búsqueda): {filter_dci_busqueda}")
    if filter_concentracion:
        mme = mme.filter(concentracion__icontains=filter_concentracion)
        filtros_aplicados.append(f"Concentración: {filter_concentracion}")
    if filter_forma_farmaceutica:
        mme = mme.filter(forma_farmaceutica=filter_forma_farmaceutica)
        filtros_aplicados.append(f"Forma Farmacéutica: {filter_forma_farmaceutica}")
    if filter_nota:
        mme = mme.filter(nota=filter_nota)
        filtros_aplicados.append(f"Nota: {filter_nota}")
    if filter_cum:
        mme = mme.filter(codigo_cum__icontains=filter_cum)
        filtros_aplicados.append(f"Código CUM: {filter_cum}")


    paginator = Paginator(mme, 20)
    page_number = request.GET.get('page')
    mme_page = paginator.get_page(page_number)

    
    # Formas farmacéuticas únicas
    formas_farmaceuticas = med_monopolio_estado.objects.values_list('forma_farmaceutica', flat=True).distinct().order_by('forma_farmaceutica')
    # Notas
    notas = med_monopolio_estado.objects.values_list('nota', flat=True).distinct().order_by('nota')

    context = {
        'mme': mme_page,
        'info_page' : mme_page,
        'formas_farmaceuticas': formas_farmaceuticas,
        'notas': notas,
        'filtros_aplicados': filtros_aplicados,
        'page_title': 'Monopolio'
    }
    
    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/med_monopolio_table.html', {'mme': mme_page})
        return JsonResponse({'html': html})

    return render(request, 'med_monopolio.html', context)
