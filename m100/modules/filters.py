from django.db.models import Q

def apply_filters_tablero(proveedores_contratados, request):
    """
    Aplica los filtros recibidos en el request al queryset de proveedores contratados.
    """
    filter_nit = request.GET.get('nit')
    filter_nombre = request.GET.get('nombre')
    filter_tipo_proveedor = request.GET.get('tipo_proveedor')
    filter_numero_contrato = request.GET.get('numero_contrato')
    filter_year_contrato = request.GET.get('year_contrato')
    filter_sucursal = request.GET.get('sucursal')
    filter_supervisor = request.GET.get('supervisor')
    filter_categoria_cuentas_medicas = request.GET.get('categoria_cuentas_medicas')
    filter_habilitacion_sede = request.GET.get('codigo_de_habilitacion')
    filter_numero_sede = request.GET.get('numero_sede')
    filter_departamento = request.GET.get('departamento')
    filter_municipio = request.GET.get('municipio')
    filter_ese = request.GET.get('ese')
    filter_serv_codigo = request.GET.get('serv_codigo')
    filter_serv_nombre = request.GET.get('serv_nombre')
    filter_grse_codigo = request.GET.get('grse_codigo')
    filter_grse_nombre = request.GET.get('grse_nombre')
    filter_modalidad_intramural = request.GET.get('modalidad_intramural')
    filter_modalidad_unidad_movil = request.GET.get('modalidad_unidad_movil')
    filter_modalidad_domiciliario = request.GET.get('modalidad_domiciliario')
    filter_modalidad_jornada_salud = request.GET.get('modalidad_jornada_salud')
    filter_modalidad_telemedicina_interactiva = request.GET.get('telemedicina_interactiva')
    filter_modalidad_telemedicina_no_interactiva = request.GET.get('telemedicina_no_interactiva')
    filter_modalidad_tele_experticia = request.GET.get('modalidad_tele_experticia')
    filter_modalidad_tele_monitoreo = request.GET.get('modalidad_tele_monitoreo')

    filtros_aplicados = []

    if filter_nit:
        proveedores_contratados = proveedores_contratados.filter(nit__icontains=filter_nit)
        filtros_aplicados.append(f"NIT: {filter_nit}")
    if filter_nombre:
        proveedores_contratados = proveedores_contratados.filter(nombre__icontains=filter_nombre)
        filtros_aplicados.append(f"Razón Social: {filter_nombre}")
    if filter_tipo_proveedor:
        proveedores_contratados = proveedores_contratados.filter(tipo_proveedor=filter_tipo_proveedor)
        filtros_aplicados.append(f"Tipo de Proveedor: {filter_tipo_proveedor}")
    if filter_numero_contrato:
        proveedores_contratados = proveedores_contratados.filter(numero_contrato=filter_numero_contrato)
        filtros_aplicados.append(f"Número de Contrato: {filter_numero_contrato}")
    if filter_year_contrato:
        proveedores_contratados = proveedores_contratados.filter(year_contrato=filter_year_contrato)
        filtros_aplicados.append(f"Año Contrato: {filter_year_contrato}")
    if filter_sucursal:
        proveedores_contratados = proveedores_contratados.filter(sucursal=filter_sucursal)
        filtros_aplicados.append(f"Sucursal: {filter_sucursal}")
    if filter_supervisor:
        proveedores_contratados = proveedores_contratados.filter(supervisor=filter_supervisor)
        filtros_aplicados.append(f"Supervisor: {filter_supervisor}")
    if filter_categoria_cuentas_medicas:
        proveedores_contratados = proveedores_contratados.filter(categoria_cuentas_medicas=filter_categoria_cuentas_medicas)
        filtros_aplicados.append(f"Categoría Cuentas Médicas: {filter_categoria_cuentas_medicas}")
    if filter_habilitacion_sede:
        proveedores_contratados = proveedores_contratados.filter(codigo_de_habilitacion=filter_habilitacion_sede)
        filtros_aplicados.append(f"Código de Habilitación: {filter_habilitacion_sede}")
    if filter_numero_sede:
        proveedores_contratados = proveedores_contratados.filter(numero_sede=filter_numero_sede)
        filtros_aplicados.append(f"Número de Sede: {filter_numero_sede}")
    if filter_departamento:
        proveedores_contratados = proveedores_contratados.filter(departamento=filter_departamento)
        filtros_aplicados.append(f"Departamento: {filter_departamento}")
    if filter_municipio:
        proveedores_contratados = proveedores_contratados.filter(municipio=filter_municipio)
        filtros_aplicados.append(f"Municipio: {filter_municipio}")
    if filter_ese:
        proveedores_contratados = proveedores_contratados.filter(ese=filter_ese)
        filtros_aplicados.append(f"Es una ESE: {filter_ese}")
    if filter_serv_codigo:
        proveedores_contratados = proveedores_contratados.filter(serv_codigo=filter_serv_codigo)
        filtros_aplicados.append(f"Servicio Codigo: {filter_serv_codigo}")
    if filter_serv_nombre:
        proveedores_contratados = proveedores_contratados.filter(serv_nombre__icontains=filter_serv_nombre)
        filtros_aplicados.append(f"Servicio Nombre: {filter_serv_nombre}")
    if filter_grse_codigo:
        proveedores_contratados = proveedores_contratados.filter(grse_codigo=filter_grse_codigo)
        filtros_aplicados.append(f"GRSE Codigo: {filter_grse_codigo}")
    if filter_grse_nombre:
        proveedores_contratados = proveedores_contratados.filter(grse_nombre__icontains=filter_grse_nombre)
        filtros_aplicados.append(f"GRSE Nombre: {filter_grse_nombre}")
    if filter_modalidad_intramural:
        proveedores_contratados = proveedores_contratados.filter(modalidad_intramural=filter_modalidad_intramural)
        filtros_aplicados.append(f"Modalidad Intramural: {filter_modalidad_intramural}")
    if filter_modalidad_unidad_movil:
        proveedores_contratados = proveedores_contratados.filter(modalidad_unidad_movil=filter_modalidad_unidad_movil)
        filtros_aplicados.append(f"Modalidad Unidad Movil: {filter_modalidad_unidad_movil}")
    if filter_modalidad_domiciliario:
        proveedores_contratados = proveedores_contratados.filter(modalidad_domiciliario=filter_modalidad_domiciliario)
        filtros_aplicados.append(f"Modalidad Domiciliario: {filter_modalidad_domiciliario}")
    if filter_modalidad_jornada_salud:
        proveedores_contratados = proveedores_contratados.filter(modalidad_jornada_salud=filter_modalidad_jornada_salud)
        filtros_aplicados.append(f"Modalidad Jornada Salud: {filter_modalidad_jornada_salud}")
    if filter_modalidad_telemedicina_interactiva:
        proveedores_contratados = proveedores_contratados.filter(telemedicina_interactiva=filter_modalidad_telemedicina_interactiva)
        filtros_aplicados.append(f"Modalidad Telemedicina Interactiva: {filter_modalidad_telemedicina_interactiva}")
    if filter_modalidad_telemedicina_no_interactiva:
        proveedores_contratados = proveedores_contratados.filter(telemedicina_no_interactiva=filter_modalidad_telemedicina_no_interactiva)
        filtros_aplicados.append(f"Modalidad Telemedicina No Interactiva: {filter_modalidad_telemedicina_no_interactiva}")
    if filter_modalidad_tele_experticia:
        proveedores_contratados = proveedores_contratados.filter(modalidad_tele_experticia=filter_modalidad_tele_experticia)
        filtros_aplicados.append(f"Modalidad Tele Experticia: {filter_modalidad_tele_experticia}")
    if filter_modalidad_tele_monitoreo:
        proveedores_contratados = proveedores_contratados.filter(modalidad_tele_monitoreo=filter_modalidad_tele_monitoreo)
        filtros_aplicados.append(f"Modalidad Tele Monitoreo: {filter_modalidad_tele_monitoreo}")

    return proveedores_contratados, filtros_aplicados

def apply_filters_reps(proveedores_contratados, request):
    """
    Aplica los filtros recibidos en el request al queryset de proveedores contratados.
    """
    filter_nit = request.GET.get('nit')
    filter_nombre = request.GET.get('nombre')
    filter_habilitacion_sede = request.GET.get('codigo_de_habilitacion')
    filter_numero_sede = request.GET.get('numero_sede')
    filter_departamento = request.GET.get('departamento')
    filter_municipio = request.GET.get('municipio')
    filter_ese = request.GET.get('ese')
    filter_serv_codigo = request.GET.get('serv_codigo')
    filter_serv_nombre = request.GET.get('serv_nombre')
    filter_grse_codigo = request.GET.get('grse_codigo')
    filter_grse_nombre = request.GET.get('grse_nombre')
    filter_modalidad_intramural = request.GET.get('modalidad_intramural')
    filter_modalidad_unidad_movil = request.GET.get('modalidad_unidad_movil')
    filter_modalidad_domiciliario = request.GET.get('modalidad_domiciliario')
    filter_modalidad_jornada_salud = request.GET.get('modalidad_jornada_salud')

    if filter_nit:
        proveedores_contratados = proveedores_contratados.filter(nit__icontains=filter_nit)
    if filter_nombre:
        proveedores_contratados = proveedores_contratados.filter(nombre__icontains=filter_nombre)
    if filter_habilitacion_sede:
        proveedores_contratados = proveedores_contratados.filter(codigo_de_habilitacion=filter_habilitacion_sede)
    if filter_numero_sede:
        proveedores_contratados = proveedores_contratados.filter(numero_sede=filter_numero_sede)
    if filter_departamento:
        proveedores_contratados = proveedores_contratados.filter(departamento=filter_departamento)
    if filter_municipio:
        proveedores_contratados = proveedores_contratados.filter(municipio=filter_municipio)
    if filter_ese:
        proveedores_contratados = proveedores_contratados.filter(ese=filter_ese)
    if filter_serv_codigo:
        proveedores_contratados = proveedores_contratados.filter(serv_codigo=filter_serv_codigo)
    if filter_serv_nombre:
        proveedores_contratados = proveedores_contratados.filter(serv_nombre__icontains=filter_serv_nombre)
    if filter_grse_codigo:
        proveedores_contratados = proveedores_contratados.filter(grse_codigo=filter_grse_codigo)
    if filter_grse_nombre:
        proveedores_contratados = proveedores_contratados.filter(grse_nombre__icontains=filter_grse_nombre)
    if filter_modalidad_intramural:
        proveedores_contratados = proveedores_contratados.filter(modalidad_intramural=filter_modalidad_intramural)
    if filter_modalidad_unidad_movil:
        proveedores_contratados = proveedores_contratados.filter(modalidad_unidad_movil=filter_modalidad_unidad_movil)
    if filter_modalidad_domiciliario:
        proveedores_contratados = proveedores_contratados.filter(modalidad_domiciliario=filter_modalidad_domiciliario)
    if filter_modalidad_jornada_salud:
        proveedores_contratados = proveedores_contratados.filter(modalidad_jornada_salud=filter_modalidad_jornada_salud)

    return proveedores_contratados
