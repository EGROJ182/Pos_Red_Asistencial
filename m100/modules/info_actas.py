from collections import defaultdict
from django.db.models import Count


def info_actas_medicamentos(tabla, tabla2):
    # Consulta a Base de datos Total Actas
    total_actas_medicamentos1 = tabla.objects.values(
        'nit_proveedor',
        'nombre_del_proveedor_pactado',
        'numero_acta_inicial',
        'fecha_pactada'
    ).annotate(total_moleculas=Count('cums_canal')).order_by('-fecha_pactada').filter(status__icontains=1)
    
    total_actas_medicamentos2 = tabla2.objects.values(
        'nit_proveedor',
        'nombre_del_proveedor_pactado',
        'numero_acta_inicial',
        'fecha_pactada'
    ).annotate(total_moleculas=Count('cums_canal')).order_by('-fecha_pactada').filter(status__icontains=1)

    total_actas_medicamentos = total_actas_medicamentos1.union(total_actas_medicamentos2)

    return total_actas_medicamentos
def info_actas_otros(tabla, tabla2):
    # Consulta a Base de datos Total Actas
    total_actas_medicamentos1 = tabla.objects.values(
        'nit_proveedor',
        'nombre_del_proveedor_pactado',
        'numero_acta_inicial',
        'fecha_pactada'
    ).annotate(total_moleculas=Count('cum')).order_by('-fecha_pactada').filter(status__icontains=1)
    
    total_actas_medicamentos2 = tabla2.objects.values(
        'nit_proveedor',
        'nombre_del_proveedor_pactado',
        'numero_acta_inicial',
        'fecha_pactada'
    ).annotate(total_moleculas=Count('cum')).order_by('-fecha_pactada').filter(status__icontains=1)

    total_actas_medicamentos = total_actas_medicamentos1.union(total_actas_medicamentos2)

    return total_actas_medicamentos

def info_actas_medicamentos_fh(tabla):
    # Consulta a Base de datos Total Actas
    total_actas_medicamentos = tabla.objects.values(
        'nit_proveedor',
        'nombre_del_proveedor_pactado',
        'numero_acta_inicial',
        'fecha_pactada'
    ).annotate(total_moleculas=Count('cums_canal')).order_by('fecha_pactada').filter(status__icontains=1)

    return total_actas_medicamentos

def info_actas_otros_fh(tabla):
    # Consulta a Base de datos Total Actas
    total_actas_medicamentos = tabla.objects.values(
        'nit_proveedor',
        'nombre_del_proveedor_pactado',
        'numero_acta_inicial',
        'fecha_pactada'
    ).annotate(total_moleculas=Count('cum')).order_by('-fecha_pactada').filter(status__icontains=1)

    return total_actas_medicamentos
