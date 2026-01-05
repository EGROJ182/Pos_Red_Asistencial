from django.db.models import Count, F
from django.db.models.functions import Concat
from django.db.models import Q

# Create your views here.
def obtener_info_reps(reps, proveedores):
    """
    Organiza la información de REPS y proveedores en un diccionario estructurado.
    
    Parámetros:
        reps: QuerySet con los registros de la tabla de REPS
        proveedores: QuerySet con los registros de proveedores contratados
    
    Retorna:
        dict: Diccionario estructurado con información de REPS y estado de contratación
    """
    # Crear un diccionario para acceder rápidamente a los proveedores por NIT
    proveedores_por_nit = {}
    for proveedor in proveedores:
        if proveedor.nit not in proveedores_por_nit:
            proveedores_por_nit[proveedor.nit] = []
        proveedores_por_nit[proveedor.nit].append(proveedor)
    
    # Diccionario principal para almacenar los resultados
    data_reps = {}
    
    # Recorrer todos los registros de REPS
    for reg in reps:
        nit = reg.nit
        
        # Si este NIT no está en el diccionario principal, agregarlo
        if nit not in data_reps:
            # Verificar si el NIT está en los proveedores contratados
            estado = "No Contratado"
            if nit in proveedores_por_nit:
                # Tomar el primer contrato (si hay varios) para el estado
                proveedor = proveedores_por_nit[nit][0]
                estado = f"{proveedor.numero_contrato}-{proveedor.year_contrato}"
                
            # Crear la entrada inicial para este NIT
            data_reps[nit] = {
                "nombre": reg.nombre,
                "nit": nit,
                "estado": estado,
                "sedes": {}
            }
        
        # Crear la clave única para el código de habilitación y sede
        chns = f"{reg.codigo_de_habilitacion}-{reg.numero_sede}"
        
        # Si esta sede no está registrada para este NIT, agregarla
        if chns not in data_reps[nit]["sedes"]:
            data_reps[nit]["sedes"][chns] = {
                "codigo_de_habilitacion": reg.codigo_de_habilitacion,
                "numero_sede": reg.numero_sede,
                "sede_nombre": reg.sede_nombre,
                "departamento": reg.departamento,
                "municipio": reg.municipio,
                "complejidad": set(),  # Usar un conjunto para complejidades únicas
                "reps": []
            }
        
        # Agregar complejidad (si no está ya agregada y no es vacía)
        if hasattr(reg, 'complejidades') and reg.complejidades and reg.complejidades.strip():
            data_reps[nit]["sedes"][chns]["complejidad"].add(reg.complejidades)
        
        # Agregar información de servicio REPS
        servicio_info = {
            "serv_codigo": reg.serv_codigo,
            "serv_nombre": reg.serv_nombre,
            "grse_codigo": reg.grse_codigo,
            "grse_nombre": reg.grse_nombre
        }
        
        # Verificar si este servicio ya está registrado para evitar duplicados
        if servicio_info not in data_reps[nit]["sedes"][chns]["reps"]:
            data_reps[nit]["sedes"][chns]["reps"].append(servicio_info)
    
    # Convertir los conjuntos de complejidad a listas para facilitar su uso
    for nit in data_reps:
        for chns in data_reps[nit]["sedes"]:
            data_reps[nit]["sedes"][chns]["complejidad"] = list(data_reps[nit]["sedes"][chns]["complejidad"])
    
    print(data_reps)
    
    return data_reps