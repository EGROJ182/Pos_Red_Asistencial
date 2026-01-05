# Exportar copia de lo cargado
import os
from django.conf import settings
from django.core.files.storage import default_storage
# Import para GET
from ..models.models_proveedores import proveedores
# Import para Post
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from ..models.models_med_homeopatica import m100fh as m100
import pandas as pd
from io import BytesIO
# Import Validaciones y Campos que no estoy tomando
from ..modules.data_load_med import nit

def loadMedHomeopatica(request):
    print('iniciamos')
    if request.method == 'POST':
        print('POST')
        # Extrae los datos del formulario
        fecha_pactada = request.POST.get('fecha_pactada')
        proveedor = request.POST.get('nombre_del_proveedor_pactado')
        numero_acta_inicial = request.POST.get('numero_acta_inicial')

        print(f"Datos del formulario: {request.POST}")

        # Extrae el archivo Excel
        excel_file = request.FILES.get('file')

        print(f"Archivos recibidos: {request.FILES}")
        
        if not excel_file:
            return JsonResponse({"error": "No se ha cargado ningún archivo"}, status=400)

        # Lee el archivo Excel usando pandas
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return JsonResponse({"error": f"Error al procesar el archivo: {str(e)}"}, status=400)

        # Procesa el archivo y genera las columnas adicionales
        print('procesando')
        df['cums_canal'] = df['cum'].astype(str) + '-' + df['canal'].astype(str)
        df['nit_proveedor'] = nit(proveedor)
        df['nombre_del_proveedor_pactado'] = proveedor
        df['numero_acta_inicial'] = numero_acta_inicial
        df['fecha_pactada'] = fecha_pactada

         # Verifica si ya existe un registro con el mismo proveedor, número de acta y fecha
        existing_records = m100.objects.filter(
            nombre_del_proveedor_pactado=proveedor,
            numero_acta_inicial=numero_acta_inicial,
            fecha_pactada=fecha_pactada
        )

        if existing_records.exists():
            return JsonResponse(
                {"error": 
                 f"Ya existen {existing_records.count()} registros con el proveedor: {proveedor}, número de acta: {numero_acta_inicial} y fecha: {fecha_pactada}."
                },status=400)

        # Ejemplo: Guarda en la base de datos o prepara los datos para respuesta
        # Aquí puedes hacer un loop para guardar los registros en tu modelo
        data_to_save = []
        for _, row in df.iterrows():
            data_to_save.append(
                m100(
                    cums_canal=row['cums_canal'],
                    tipo = 'MEDICAMENTOS',
                    descripcion_medicamento=row['descripcion_medicamento'],
                    marca=row['marca'],
                    principio_activo=row['principio_activo'],
                    concentracion=row['concentracion'],
                    forma_farmaceutica=row['forma_farmaceutica'],
                    presentacion=row['presentacion'],
                    registro_sanitario=row['registro_sanitario'],
                    estado_registro=row['estado_registro'],
                    atc = row['atc'],
                    cum = row['cum'],
                    expediente = row['expediente'],
                    consecutivo = row['consecutivo'],
                    codigo_cum_homologo=row['codigo_cum_homologo'],
                    alianza=row['alianza'],
                    laboratorio_alianza=row['laboratorio_alianza'],
                    canal=row['canal'],
                    cantidad_minima_de_dispensacion=row['cantidad_minima_de_dispensacion'],
                    variable_cantidad_unidad_minima_negociada=row['variable_cantidad_unidad_minima_negociada'],
                    valor_medicamento_regulado=row['valor_medicamento_regulado'],
                    tarifa_pactada_por_unidad_sin_iva=row['tarifa_pactada_por_unidad_sin_iva'],
                    medicamentos_de_control_especial=row['medicamentos_de_control_especial'],
                    medicamentos_monopolio_del_estado=row['medicamentos_monopolio_del_estado'],
                    nit_proveedor=row['nit_proveedor'],
                    nombre_del_proveedor_pactado=row['nombre_del_proveedor_pactado'],
                    numero_acta_inicial=row['numero_acta_inicial'],
                    fecha_pactada=row['fecha_pactada'],
                    validador_acta_duplicada='', # se eliminara porque no se va permitir cargar actas duplicadas
                    circular_valor_regulado='', # realizar operacion para validar a cual valor de circular aplica
                    precio_maximo_final_institucional='', # realizar operacion para validar el maximo institucional regulado del cum
                    precio_maximo_final_comercial='', # realizar operacion para validar el maximo comercial regulado del cum
                    status_invima='', # realizar operacion para validar el estado del invima en base invima
                    validador_precio_mismo_canal='', # realizar operacion para validar el precio del mismo canal
                    precio_regulado_institucional_2022='', # realizar operacion para validar el precio regulado del 2022
                    novedad='prueba' # realizar analisis de las novedades
                )
            )
        
        # Guarda en la base de datos (esto puede variar según tu implementación)
        m100.objects.bulk_create(data_to_save)

        file_name = f'acta_{numero_acta_inicial}_{proveedor}_med.xlsx'

        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        # Guarda el archivo Excel en MEDIA_ROOT
        with default_storage.open(file_path, 'wb') as f:
            df.to_excel(f, index=False, engine='openpyxl')
        
        # Genera la URL para que el archivo sea descargable desde el frontend
        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
        
        # Retorna un JSON con la URL del archivo para permitir su descarga
        return JsonResponse({"file_url": file_url, "num_records": len(data_to_save)})

        # Devuelve la respuesta JSON con el número de registros cargados
        # return JsonResponse({"success": "Archivo cargado y procesado exitosamente", "num_records": len(data_to_save)})
    
    
    # Proveedores únicos
    nombres = proveedores.objects.filter(tipo_proveedor="PRESTADOR DE TECNOLOGÍAS EN SALUD").values_list('nombre', flat=True).distinct().order_by('nombre')
    # Tipos de proveedor
    pts = proveedores.objects.filter(tipo_proveedor="PRESTADOR DE TECNOLOGÍAS EN SALUD")
    pss = proveedores.objects.filter(tipo_proveedor="PRESTADOR DE SERVICIOS DE SALUD")
    otros = proveedores.objects.filter(tipo_proveedor="otro")

    # Número Actas
    actas = ['Estandar']

    for acta in range(1, 300):
        actas.append(acta)

    context = {
        'pts': pts,
        'pss': pss,
        'otros': otros,
        'nombres': nombres,
        'numero_acta': actas,
        'page_title': 'Cargue Actas'
    }

    return render(request, 'load_med_homeopatica.html', context)
