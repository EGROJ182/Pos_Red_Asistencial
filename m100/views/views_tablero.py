from django.shortcuts import render
from ..models.models_tablero_gerencia import Tablero as Proveedores
from ..modules.alert import alert
from django.http import JsonResponse
from django.db.models import Count

def tablero(request):
    proveedores_contratados = Proveedores.objects.all()
    context = {
        'proveedores': proveedores_contratados,
        'alerts': alert(Proveedores),
        'page_title': 'Tablero Gerencia Médica'
    }
    return render(request, 'tablero_gerencia.html', context)


def proveedores_data(request):
    queryset = Proveedores.objects.values('departamento').annotate(total=Count('nit'))
    data = {
        'labels': [item['departamento'] for item in queryset],
        'values': [item['total'] for item in queryset],
    }
    return JsonResponse(data)


def proveedores_map_data(request):
    """
    Retorna la lista de proveedores con su latitud, longitud y
    cualquier otra info que quieras mostrar en el popup.
    """
    queryset = Proveedores.objects.values('nit', 'nombre', 'departamento', 'latitud', 'longitud')
    data = list(queryset)  # Convertimos QuerySet a lista de dicts
    return JsonResponse(data, safe=False)