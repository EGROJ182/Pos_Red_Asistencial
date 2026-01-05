from django.core.paginator import Paginator
from ..models.models_proveedores import proveedores
from ..models.models_med_vigente import m100Vigente
from ..models.models_med_antigua import m100Antigua
from django.shortcuts import render
from django.template.loader import render_to_string
from ..modules.color_cell_alert import alert_color
from django.http import JsonResponse

# Create your views here.
def nit(nombre_del_proveedor_pactado):
    nit = proveedores.objects.filter(nombre=nombre_del_proveedor_pactado).values_list('nit', flat=True).distinct().order_by('nit').first()
    print(nit)
    return nit