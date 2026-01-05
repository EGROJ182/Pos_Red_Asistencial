from ..models.models_med_vigente import m100Vigente
from ..models.models_others_vigente import OthersVigente
from ..models.models_med_col import m100Col as m100Colsub
from ..models.models_others_col import OthersCol as otrosColsub
from django.db.models import Count, F
from django.db.models.functions import Concat
from django.db.models import Q

# Create your views here.
# def obtener_datos_estandar(m100Vigente, OthersVigente, colsubMed, colsubOtros):
def obtener_datos_estandar(m100Vigente, OthersVigente):
    # Agregar sumas de los campos necesarios
    # m100Vigente.objects.values('nit_proveedor', 'nombre_del_proveedor_pactado') para realizarlo con values, depende de la cantidad de datos
    # .annotate(total_cums_m100=Count('cums_canal'))
    # Usamos select_related para obtener los datos relacionados de la base de datos en una sola consulta.
    medicamentos = (
        m100Vigente.objects.filter(status=1).select_related('nombre_del_proveedor_pactado')  # Optimiza la relación
        .values('nit_proveedor', 'nombre_del_proveedor_pactado')
        .annotate(total_cums_m100=Count('cums_canal', distinct=True))
    )
    # medicamentos = (
    #     m100Vigente.objects.select_related('nombre_del_proveedor_pactado')  # Optimiza la relación
    #     .values('nit_proveedor', 'nombre_del_proveedor_pactado')
    #     .annotate(total_cums_m100=Count('cums_canal', distinct=True))
    # )
    # med_colsub = (
    #     colsubMed.objects.select_related('nombre_del_proveedor_pactado')  # Optimiza la relación
    #     .values('nit_proveedor', 'nombre_del_proveedor_pactado')
    #     .annotate(total_cums_m100=Count('cums_canal', distinct=True))
    # )
    
    otros = (
        OthersVigente.objects.filter(status=1).select_related('nombre_del_proveedor_pactado')  # También aquí
        .values('nit_proveedor', 'nombre_del_proveedor_pactado')
        .annotate(total_cums_otros=Count('cum', distinct=True))
    )
    # otros = (
    #     OthersVigente.objects.select_related('nombre_del_proveedor_pactado')  # También aquí
    #     .values('nit_proveedor', 'nombre_del_proveedor_pactado')
    #     .annotate(total_cums_otros=Count('cum', distinct=True))
    # )
    # otros_colsub = (
    #     colsubOtros.objects.select_related('nombre_del_proveedor_pactado')  # También aquí
    #     .values('nit_proveedor', 'nombre_del_proveedor_pactado')
    #     .annotate(total_cums_otros=Count('cum', distinct=True))
    # )

    # Crear un diccionario para almacenar los resultados agrupados
    resultados = {}

    # Procesar los medicamentos
    for medicamento in medicamentos:
        nit_proveedor = medicamento['nit_proveedor']
        nombre_del_proveedor_pactado = medicamento['nombre_del_proveedor_pactado']
        total_cums_m100 = medicamento['total_cums_m100'] or 0  # Manejar valores nulos

        # Inicializar el diccionario para cada proveedor
        if nit_proveedor not in resultados:
            resultados[nit_proveedor] = {}
        if nombre_del_proveedor_pactado not in resultados[nit_proveedor]:
            resultados[nit_proveedor][nombre_del_proveedor_pactado] = {
                'total_cums_m100': 0,
                'total_cums_otros': 0,
                'suma_total_cums': 0
            }

        resultados[nit_proveedor][nombre_del_proveedor_pactado]['total_cums_m100'] += total_cums_m100

    # Procesar los otros
    for otro in otros:
        nit_proveedor = otro['nit_proveedor']
        nombre_del_proveedor_pactado = otro['nombre_del_proveedor_pactado']
        total_cums_otros = otro['total_cums_otros'] or 0  # Manejar valores nulos

        # Inicializar el diccionario para cada proveedor
        if nit_proveedor not in resultados:
            resultados[nit_proveedor] = {}
        if nombre_del_proveedor_pactado not in resultados[nit_proveedor]:
            resultados[nit_proveedor][nombre_del_proveedor_pactado] = {
                'total_cums_m100': 0,
                'total_cums_otros': 0,
                'suma_total_cums': 0
            }

        resultados[nit_proveedor][nombre_del_proveedor_pactado]['total_cums_otros'] += total_cums_otros

    # Procesar los med colsub
    # for medicamento in med_colsub:
    #     nit_proveedor = medicamento['nit_proveedor']
    #     nombre_del_proveedor_pactado = medicamento['nombre_del_proveedor_pactado']
    #     total_cums_m100 = medicamento['total_cums_m100'] or 0  # Manejar valores nulos

    #     # Inicializar el diccionario para cada proveedor
    #     if nit_proveedor not in resultados:
    #         resultados[nit_proveedor] = {}
    #     if nombre_del_proveedor_pactado not in resultados[nit_proveedor]:
    #         resultados[nit_proveedor][nombre_del_proveedor_pactado] = {
    #             'total_cums_m100': 0,
    #             'total_cums_otros': 0,
    #             'suma_total_cums': 0
    #         }

    #     resultados[nit_proveedor][nombre_del_proveedor_pactado]['total_cums_m100'] += total_cums_m100

    # # Procesar los otros colsub
    # for otro in otros_colsub:
    #     nit_proveedor = otro['nit_proveedor']
    #     nombre_del_proveedor_pactado = otro['nombre_del_proveedor_pactado']
    #     total_cums_otros = otro['total_cums_otros'] or 0  # Manejar valores nulos

    #     # Inicializar el diccionario para cada proveedor
    #     if nit_proveedor not in resultados:
    #         resultados[nit_proveedor] = {}
    #     if nombre_del_proveedor_pactado not in resultados[nit_proveedor]:
    #         resultados[nit_proveedor][nombre_del_proveedor_pactado] = {
    #             'total_cums_m100': 0,
    #             'total_cums_otros': 0,
    #             'suma_total_cums': 0
    #         }

    #     resultados[nit_proveedor][nombre_del_proveedor_pactado]['total_cums_otros'] += total_cums_otros

    # Calcular la suma total de CUMs
    for nit_proveedor, proveedores in resultados.items():
        for nombre_del_proveedor_pactado, datos in proveedores.items():
            datos['suma_total_cums'] = datos['total_cums_m100'] + datos['total_cums_otros']

    # Convertir el diccionario en una lista de resultados
    lista_resultados = [
        {
            'nit_proveedor': nit_proveedor,
            'nombre_del_proveedor_pactado': nombre_del_proveedor_pactado,
            'total_cums_m100': datos['total_cums_m100'],
            'total_cums_otros': datos['total_cums_otros'],
            'suma_total_cums': datos['suma_total_cums']
        }
        for nit_proveedor, proveedores in resultados.items()
        for nombre_del_proveedor_pactado, datos in proveedores.items()
    ]

    tarifario_estandar = total_estandar(m100Vigente, OthersVigente)

    for estandar in tarifario_estandar:
        estandar['nit_proveedor'] = 'Positiva'
        estandar['nombre_del_proveedor_pactado'] = 'Anexo 1 Tarifario Estandar'
        estandar['total_cums_m100'] = estandar['medicamentos']
        estandar['total_cums_otros'] = estandar['otros']
        estandar['suma_total_cums'] = estandar['total_cums']

    # Agregar el tarifario estandar al final de la lista
    lista_resultados.extend(tarifario_estandar)

    # Ordenar la lista de resultados de mayor a menor
    lista_resultados.sort(key=lambda x: x['suma_total_cums'], reverse=True)

    # Ordenar por nit_proveedor y nombre_del_proveedor_pactado
    # lista_resultados.sort(key=lambda x: (x['nombre_del_proveedor_pactado'], x['nit_proveedor']))

    return lista_resultados

def obtener_datos_estandar_fh(m100Vigente, OthersVigente):
    # Agregar sumas de los campos necesarios
    # m100Vigente.objects.values('nit_proveedor', 'nombre_del_proveedor_pactado') para realizarlo con values, depende de la cantidad de datos
    # .annotate(total_cums_m100=Count('cums_canal'))
    # Usamos select_related para obtener los datos relacionados de la base de datos en una sola consulta.
    medicamentos = (
        m100Vigente.objects.filter(status=1).select_related('nombre_del_proveedor_pactado')  # Optimiza la relación
        .values('nit_proveedor', 'nombre_del_proveedor_pactado')
        .annotate(total_cums_m100=Count('cums_canal', distinct=True))
    )
    
    otros = (
        OthersVigente.objects.filter(status=1).select_related('nombre_del_proveedor_pactado')  # También aquí
        .values('nit_proveedor', 'nombre_del_proveedor_pactado')
        .annotate(total_cums_otros=Count('cum', distinct=True))
    )

    # Crear un diccionario para almacenar los resultados agrupados
    resultados = {}

    # Procesar los medicamentos
    for medicamento in medicamentos:
        nit_proveedor = medicamento['nit_proveedor']
        nombre_del_proveedor_pactado = medicamento['nombre_del_proveedor_pactado']
        total_cums_m100 = medicamento['total_cums_m100'] or 0  # Manejar valores nulos

        # Inicializar el diccionario para cada proveedor
        if nit_proveedor not in resultados:
            resultados[nit_proveedor] = {}
        if nombre_del_proveedor_pactado not in resultados[nit_proveedor]:
            resultados[nit_proveedor][nombre_del_proveedor_pactado] = {
                'total_cums_m100': 0,
                'total_cums_otros': 0,
                'suma_total_cums': 0
            }

        resultados[nit_proveedor][nombre_del_proveedor_pactado]['total_cums_m100'] += total_cums_m100

    # Procesar los otros
    for otro in otros:
        nit_proveedor = otro['nit_proveedor']
        nombre_del_proveedor_pactado = otro['nombre_del_proveedor_pactado']
        total_cums_otros = otro['total_cums_otros'] or 0  # Manejar valores nulos

        # Inicializar el diccionario para cada proveedor
        if nit_proveedor not in resultados:
            resultados[nit_proveedor] = {}
        if nombre_del_proveedor_pactado not in resultados[nit_proveedor]:
            resultados[nit_proveedor][nombre_del_proveedor_pactado] = {
                'total_cums_m100': 0,
                'total_cums_otros': 0,
                'suma_total_cums': 0
            }

        resultados[nit_proveedor][nombre_del_proveedor_pactado]['total_cums_otros'] += total_cums_otros


    # Calcular la suma total de CUMs
    for nit_proveedor, proveedores in resultados.items():
        for nombre_del_proveedor_pactado, datos in proveedores.items():
            datos['suma_total_cums'] = datos['total_cums_m100'] + datos['total_cums_otros']

    # Convertir el diccionario en una lista de resultados
    lista_resultados = [
        {
            'nit_proveedor': nit_proveedor,
            'nombre_del_proveedor_pactado': nombre_del_proveedor_pactado,
            'total_cums_m100': datos['total_cums_m100'],
            'total_cums_otros': datos['total_cums_otros'],
            'suma_total_cums': datos['suma_total_cums']
        }
        for nit_proveedor, proveedores in resultados.items()
        for nombre_del_proveedor_pactado, datos in proveedores.items()
    ]

    tarifario_estandar = total_estandar(m100Vigente, OthersVigente)

    for estandar in tarifario_estandar:
        estandar['nit_proveedor'] = 'Positiva'
        estandar['nombre_del_proveedor_pactado'] = 'Anexo 1 Tarifario Estandar'
        estandar['total_cums_m100'] = estandar['medicamentos']
        estandar['total_cums_otros'] = estandar['otros']
        estandar['suma_total_cums'] = estandar['total_cums']

    # Agregar el tarifario estandar al final de la lista
    lista_resultados.extend(tarifario_estandar)

    # Ordenar la lista de resultados de mayor a menor
    lista_resultados.sort(key=lambda x: x['suma_total_cums'], reverse=True)

    # Ordenar por nit_proveedor y nombre_del_proveedor_pactado
    # lista_resultados.sort(key=lambda x: (x['nombre_del_proveedor_pactado'], x['nit_proveedor']))

    return lista_resultados


def total_estandar(m100Vigente, OthersVigente):
    # Contar los valores únicos de cums_canal en m100Vigente
    total_cums_m100 = m100Vigente.objects.filter(status=1).values('cums_canal').distinct().count()

    # Contar los valores únicos de cum en OthersVigente
    total_cums_otros = OthersVigente.objects.filter(status=1).values('cum').distinct().count()

    # Calcular el total de cums
    total_cums = total_cums_m100 + total_cums_otros

    # Retornar el resultado como una lista con un diccionario
    return [
        {
            'medicamentos': total_cums_m100,
            'otros': total_cums_otros,
            'total_cums': total_cums
        }
    ]