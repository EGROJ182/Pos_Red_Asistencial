from django.shortcuts import render
from django.shortcuts import render
from ..models.models_proveedores import proveedores
from datetime import datetime

# Create your views here.
def home(request):
    # try:
    #     # Obtener todos los proveedores
    #     proveedores_contratados = proveedores.objects.all()
    # except Exception as e:
    #     # En caso de error, inicializar una lista vacía
    #     proveedores_contratados = []

    # # Lista para almacenar los proveedores que cumplen con la condición
    # proveedores_filtrados = []

    # for proveedor in proveedores_contratados:
    #     fecha_fin_contrato = proveedor.fecha_fin_contrato

    #     if not fecha_fin_contrato or fecha_fin_contrato.strip() == '':
    #         proveedor.dias_restantes = 'Sin fecha'
    #     elif fecha_fin_contrato.lower() == 'renovacion automatica':
    #         proveedor.dias_restantes = 'Renovación Automática'
    #     else:
    #         try:
    #             # Convertir la fecha a un objeto date
    #             fecha_fin = datetime.strptime(fecha_fin_contrato, '%Y-%m-%d').date()
    #             hoy = datetime.now().date()
    #             dias_restantes = (fecha_fin - hoy).days
    #             proveedor.dias_restantes = dias_restantes
    #         except ValueError:
    #             proveedor.dias_restantes = 'Fecha inválida'

    #     # Filtrar proveedores: eliminar aquellos con días restantes > 31
    #     if isinstance(proveedor.dias_restantes, int) and proveedor.dias_restantes <= 31:
    #         proveedores_filtrados.append(proveedor)

    # # Pasar los proveedores filtrados al contexto
    # context = {
    #     'proveedores': proveedores_filtrados,
    # }

    return render(request, 'home.html')