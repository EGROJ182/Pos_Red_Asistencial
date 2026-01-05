import locale
from datetime import datetime

# Configurar localización en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Create your views here.
def alert(proveedores):
    try:
        # Obtener todos los proveedores
        proveedores_contratados = proveedores.objects.all().order_by('nombre')
    except Exception as e:
        # En caso de error, inicializar una lista vacía
        proveedores_contratados = [str(e)]

    # Lista para almacenar los proveedores que cumplen con la condición
    proveedores_filtrados = []

    if len(proveedores_contratados) == 0:
        return proveedores_filtrados

    for proveedor in proveedores_contratados:
            fecha_fin_contrato = proveedor.fecha_fin_contrato

            if not fecha_fin_contrato or fecha_fin_contrato.strip() == '':
                proveedor.dias_restantes = 'Sin fecha'
                proveedor.fecha_real = 'Sin fecha'
            elif fecha_fin_contrato.lower() == 'renovacion automatica':
                proveedor.dias_restantes = 'Renovación Automática'
                proveedor.fecha_real = 'Renovación Automática'
            else:
                try:
                    # Convertir la fecha a un objeto date
                    fecha_fin = datetime.strptime(fecha_fin_contrato, '%Y-%m-%d').date()
                    hoy = datetime.now().date()
                    dias_restantes = (fecha_fin - hoy).days
                    proveedor.dias_restantes = dias_restantes

                    # Calcular la fecha real sumando los días restantes a hoy
                    proveedor.fecha_real = fecha_fin.strftime('%A %d de %B de %Y')

                except ValueError:
                    proveedor.dias_restantes = 'Fecha inválida'
                    proveedor.fecha_real = 'Fecha inválida'

            # Filtrar proveedores: eliminar aquellos con días restantes > 31
            if isinstance(proveedor.dias_restantes, int) and proveedor.dias_restantes <= 30:
                proveedores_filtrados.append(proveedor)

            # Ordenar la lista filtrada por días restantes
            proveedores_filtrados_ordenados = sorted(proveedores_filtrados, key=lambda x: x.dias_restantes if isinstance(x.dias_restantes, int) else float('inf'))

            for proveedor in proveedores_filtrados_ordenados:
                if proveedor.dias_restantes < 0:
                    proveedor.bg = 'black'
                    proveedor.content = 'content-alert-black'
                    proveedor.div = 'content-div-alert-black'
                    proveedor.text = 'white'
                    proveedor.message = 'Vencido'
                elif proveedor.dias_restantes == 0:
                    proveedor.bg = 'red'
                    proveedor.content = 'content-alert-red'
                    proveedor.div = 'content-div-alert-red'
                    proveedor.text = 'white'
                    proveedor.message = f'Vence Hoy {proveedor.fecha_real}'
                elif proveedor.dias_restantes == 1:
                    proveedor.bg = 'red'
                    proveedor.content = 'content-alert-red'
                    proveedor.div = 'content-div-alert-red'
                    proveedor.text = 'white'
                    proveedor.message = f'Vence Mañana ({proveedor.fecha_real})'
                elif proveedor.dias_restantes == 2:
                    proveedor.bg = 'red'
                    proveedor.content = 'content-alert-red'
                    proveedor.div = 'content-div-alert-red'
                    proveedor.text = 'white'
                    proveedor.message = f'Vence Pasado Mañana ({proveedor.fecha_real})'
                elif proveedor.dias_restantes <= 5:
                    proveedor.bg = 'orange'
                    proveedor.content = 'content-alert-orange'
                    proveedor.div = 'content-div-alert-orange'
                    proveedor.text = 'white'
                    proveedor.message = f'Vence esta semana ({proveedor.fecha_real})'
                else:
                    proveedor.bg = 'white'
                    proveedor.content = 'content-alert-green'
                    proveedor.div = 'content-div-alert-green'
                    proveedor.text = 'black'
                    proveedor.message = f'Vence dentro de {proveedor.dias_restantes} dias el ({proveedor.fecha_real})'

    return proveedores_filtrados_ordenados
