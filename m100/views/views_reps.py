from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from ..models.models_reps import reps
from ..models.models_proveedores import proveedores
from ..modules.alert import alert


# Create your views here.
def repsView(request):
    # Obtener datos desde las bases de datos
    registro = reps.objects.using('dataTarifas').all()

    # Filtrado según los parámetros del formulario
    filter_dpto = request.GET.get('departamento')
    filter_municipio = request.GET.get('municipio')
    filter_codigo_de_habilitacion = request.GET.get('codigo_de_habilitacion')
    filter_numero_sede = request.GET.get('numero_sede')
    filter_sede_nombre = request.GET.get('sede_nombre')
    filter_direccion = request.GET.get('direccion')
    filter_telefono = request.GET.get('telefono')
    filter_email = request.GET.get('email')
    filter_nit = request.GET.get('nit')
    filter_dv_nit = request.GET.get('dv_nit')
    filter_ese = request.GET.get('ese')
    filter_grse_codigo = request.GET.get('grse_codigo')
    filter_grse_nombre = request.GET.get('grse_nombre')
    filter_serv_codigo = request.GET.get('serv_codigo')
    filter_serv_nombre = request.GET.get('serv_nombre')
    filter_ambulatorio = request.GET.get('ambulatorio')
    filter_hospitalario = request.GET.get('hospitalario')
    filter_unidad_movil = request.GET.get('unidad_movil')
    filter_domiciliario = request.GET.get('domiciliario')
    filter_nombre = request.GET.get('nombre')
    filter_modalidad_intramural = request.GET.get('modalidad_intramural')
    filter_modalidad_extramural = request.GET.get('modalidad_extramural')
    filter_modalidad_unidad_movil = request.GET.get('modalidad_unidad_movil')
    filter_modalidad_domiciliario = request.GET.get('modalidad_domiciliario')
    filter_modalidad_telemedicina = request.GET.get('modalidad_telemedicina')
    filter_modalidad_prestador_referencia = request.GET.get('modalidad_prestador_referencia')
    filter_modalidad_prestador_referencia_telemedicina_interactiva = request.GET.get('modalidad_prestador_referencia_telemedicina_interactiva')
    filter_modalidad_prestador_referencia_telemedicina_no_interactiva = request.GET.get('modalidad_prestador_referencia_telemedicina_no_interactiva')
    filter_modalidad_prestador_referencia_tele_experticia = request.GET.get('modalidad_prestador_referencia_tele_experticia')
    filter_modalidad_prestador_referencia_tele_monitoreo = request.GET.get('modalidad_prestador_referencia_tele_monitoreo')
    filter_modalidad_prestador_remisor = request.GET.get('modalidad_prestador_remisor')
    filter_modalidad_prestador_remisor_tele_experticia = request.GET.get('modalidad_prestador_remisor_tele_experticia')
    filter_modalidad_prestador_remisor_tele_monitoreo = request.GET.get('modalidad_prestador_remisor_tele_monitoreo')
    filter_complejidades = request.GET.get('complejidades')

    filtros_aplicados = []

    if filter_dpto:
        registro = registro.filter(departamento__icontains=filter_dpto)
        filtros_aplicados.append(f"Departamento: {filter_dpto}")
    if filter_municipio:
        registro = registro.filter(municipio__icontains=filter_municipio)
        filtros_aplicados.append(f"Municipio: {filter_municipio}")
    if filter_codigo_de_habilitacion:
        registro = registro.filter(codigo_de_habilitacion__icontains=filter_codigo_de_habilitacion)
        filtros_aplicados.append(f"Codigo de Habilitacion: {filter_codigo_de_habilitacion}")
    if filter_numero_sede:
        registro = registro.filter(numero_sede__icontains=filter_numero_sede)
        filtros_aplicados.append(f"Numero de Sede: {filter_numero_sede}")
    if filter_sede_nombre:
        registro = registro.filter(sede_nombre__icontains=filter_sede_nombre)
        filtros_aplicados.append(f"Sede Nombre: {filter_sede_nombre}")
    if filter_direccion:
        registro = registro.filter(direccion__icontains=filter_direccion)
        filtros_aplicados.append(f"Direccion: {filter_direccion}")
    if filter_telefono:
        registro = registro.filter(telefono__icontains=filter_telefono)
        filtros_aplicados.append(f"Telefono: {filter_telefono}")
    if filter_email:
        registro = registro.filter(email__icontains=filter_email)
        filtros_aplicados.append(f"Email: {filter_email}")
    if filter_nit:
        registro = registro.filter(nit__icontains=filter_nit)
        filtros_aplicados.append(f"NIT: {filter_nit}")
    if filter_dv_nit:
        registro = registro.filter(dv_nit__icontains=filter_dv_nit)
        filtros_aplicados.append(f"DV NIT: {filter_dv_nit}")
    if filter_ese:
        registro = registro.filter(ese__icontains=filter_ese)
        filtros_aplicados.append(f"ESE: {filter_ese}")
    if filter_grse_codigo:
        registro = registro.filter(grse_codigo__icontains=filter_grse_codigo)
        filtros_aplicados.append(f"GRSE Codigo: {filter_grse_codigo}")
    if filter_grse_nombre:
        registro = registro.filter(grse_nombre__icontains=filter_grse_nombre)
        filtros_aplicados.append(f"GRSE Nombre: {filter_grse_nombre}")
    if filter_serv_codigo:
        registro = registro.filter(serv_codigo__icontains=filter_serv_codigo)
        filtros_aplicados.append(f"SERV Codigo: {filter_serv_codigo}")
    if filter_serv_nombre:
        registro = registro.filter(serv_nombre__icontains=filter_serv_nombre)
        filtros_aplicados.append(f"SERV Nombre: {filter_serv_nombre}")
    if filter_ambulatorio:
        registro = registro.filter(ambulatorio__icontains=filter_ambulatorio)
        filtros_aplicados.append(f"Ambulatorio: {filter_ambulatorio}")
    if filter_hospitalario:
        registro = registro.filter(hospitalario__icontains=filter_hospitalario)
        filtros_aplicados.append(f"Hospitalario: {filter_hospitalario}")
    if filter_unidad_movil:
        registro = registro.filter(unidad_movil__icontains=filter_unidad_movil)
        filtros_aplicados.append(f"Unidad Movil: {filter_unidad_movil}")
    if filter_domiciliario:
        registro = registro.filter(domiciliario__icontains=filter_domiciliario)
        filtros_aplicados.append(f"Domiciliario: {filter_domiciliario}")
    if filter_nombre:
        registro = registro.filter(nombre__icontains=filter_nombre)
        filtros_aplicados.append(f"Razón Social: {filter_nombre}")
    if filter_modalidad_intramural:
        registro = registro.filter(modalidad_intramural__icontains=filter_modalidad_intramural)
        filtros_aplicados.append(f"Modalidad Intramural: {filter_modalidad_intramural}")
    if filter_modalidad_extramural:
        registro = registro.filter(modalidad_extramural__icontains=filter_modalidad_extramural)
        filtros_aplicados.append(f"Modalidad Extramural: {filter_modalidad_extramural}")
    if filter_modalidad_unidad_movil:
        registro = registro.filter(modalidad_unidad_movil__icontains=filter_modalidad_unidad_movil)
        filtros_aplicados.append(f"Modalidad Unidad Movil: {filter_modalidad_unidad_movil}")
    if filter_modalidad_domiciliario:
        registro = registro.filter(modalidad_domiciliario__icontains=filter_modalidad_domiciliario)
        filtros_aplicados.append(f"Modalidad Domiciliario: {filter_modalidad_domiciliario}")
    if filter_modalidad_telemedicina:
        registro = registro.filter(modalidad_telemedicina__icontains=filter_modalidad_telemedicina)
        filtros_aplicados.append(f"Modalidad Telemedicina: {filter_modalidad_telemedicina}")
    if filter_modalidad_prestador_referencia:
        registro = registro.filter(modalidad_prestador_referencia__icontains=filter_modalidad_prestador_referencia)
        filtros_aplicados.append(f"Modalidad Prestador Referencia: {filter_modalidad_prestador_referencia}")
    if filter_modalidad_prestador_referencia_telemedicina_interactiva:
        registro = registro.filter(modalidad_prestador_referencia_telemedicina_interactiva__icontains=filter_modalidad_prestador_referencia_telemedicina_interactiva)
        filtros_aplicados.append(f"Modalidad Prestador Referencia Telemedicina Interactiva: {filter_modalidad_prestador_referencia_telemedicina_interactiva}")
    if filter_modalidad_prestador_referencia_telemedicina_no_interactiva:
        registro = registro.filter(modalidad_prestador_referencia_telemedicina_no_interactiva__icontains=filter_modalidad_prestador_referencia_telemedicina_no_interactiva)
        filtros_aplicados.append(f"Modalidad Prestador Referencia Telemedicina No Interactiva: {filter_modalidad_prestador_referencia_telemedicina_no_interactiva}")
    if filter_modalidad_prestador_referencia_tele_experticia:
        registro = registro.filter(modalidad_prestador_referencia_tele_experticia__icontains=filter_modalidad_prestador_referencia_tele_experticia)
        filtros_aplicados.append(f"Modalidad Prestador Referencia Tele Experticia: {filter_modalidad_prestador_referencia_tele_experticia}")
    if filter_modalidad_prestador_referencia_tele_monitoreo:
        registro = registro.filter(modalidad_prestador_referencia_tele_monitoreo__icontains=filter_modalidad_prestador_referencia_tele_monitoreo)
        filtros_aplicados.append(f"Modalidad Prestador Referencia Tele Monitoreo: {filter_modalidad_prestador_referencia_tele_monitoreo}")
    if filter_modalidad_prestador_remisor:
        registro = registro.filter(modalidad_prestador_remisor__icontains=filter_modalidad_prestador_remisor)
        filtros_aplicados.append(f"Modalidad Prestador Remisor: {filter_modalidad_prestador_remisor}")
    if filter_modalidad_prestador_remisor_tele_experticia:
        registro = registro.filter(modalidad_prestador_remisor_tele_experticia__icontains=filter_modalidad_prestador_remisor_tele_experticia)
        filtros_aplicados.append(f"Modalidad Prestador Remisor Tele Experticia: {filter_modalidad_prestador_remisor_tele_experticia}")
    if filter_modalidad_prestador_remisor_tele_monitoreo:
        registro = registro.filter(modalidad_prestador_remisor_tele_monitoreo__icontains=filter_modalidad_prestador_remisor_tele_monitoreo)
        filtros_aplicados.append(f"Modalidad Prestador Remisor Tele Monitoreo: {filter_modalidad_prestador_remisor_tele_monitoreo}")
    if filter_complejidades:
        registro = registro.filter(complejidades__icontains=filter_complejidades)
        filtros_aplicados.append(f"Complejidades: {filter_complejidades}")


    prestadores = registro.values('nit', 'nombre').distinct()

    paginator = Paginator(prestadores, 20)
    page_number = request.GET.get('page')
    registros_page = paginator.get_page(page_number)

    data = []

    for prestador in registros_page:
        # Get all sedes for this prestador
        sedes = registro.filter(nit=prestador['nit']).values(
            'nit', 'nombre', 'codigo_de_habilitacion', 'numero_sede', 
            'sede_nombre', 'departamento', 'municipio', 'direccion', 'telefono', 'email'
        ).distinct()
        
        # Count the number of sedes
        cantidad_sedes = sedes.count()
        
        # Prepare data for each sede and its services
        sedes_data = []
        for sede in sedes:
            # Get all services for this sede
            servicios = registro.filter(
                nit=prestador['nit'],
                codigo_de_habilitacion=sede['codigo_de_habilitacion'],
                numero_sede=sede['numero_sede']
            ).values('serv_codigo', 'serv_nombre', 'grse_codigo', 'grse_nombre', 'complejidades').distinct()
            
            # Add services to sede data
            sede_con_servicios = {
                **sede,
                'servicios': list(servicios),
                'complejidades': list(set([s['complejidades'] for s in servicios]))
            }
            
            sedes_data.append(sede_con_servicios)
        
        # Add prestador with all its sedes and services
        prestador_completo = {
            **prestador,
            'cantidad_sedes': cantidad_sedes,
            'sedes': sedes_data
        }
        
        data.append(prestador_completo)

    # Departamentos
    dptos = reps.objects.using('dataTarifas').all().values_list('departamento', flat=True).distinct().order_by('departamento')
    # Municipios
    municipios = reps.objects.using('dataTarifas').all().values_list('municipio', flat=True).distinct().order_by('municipio')
    # Números Sedes
    n_sedes = reps.objects.using('dataTarifas').all().values_list('numero_sede', flat=True).distinct().order_by('numero_sede')
    # ESES
    eses = reps.objects.using('dataTarifas').all().values_list('ese', flat=True).distinct().order_by('ese')
    # REPS
    serv_codigos = reps.objects.using('dataTarifas').all().values('serv_codigo', 'serv_nombre').distinct().order_by('serv_codigo')
    # Grupos REPS
    grupos = reps.objects.using('dataTarifas').all().values('grse_codigo', 'grse_nombre').distinct().order_by('grse_codigo')
    # Modalidad intramural
    intramural = reps.objects.using('dataTarifas').all().values_list('modalidad_intramural', flat=True).distinct().order_by('modalidad_intramural')
    # Modalidad extramural
    extramural = reps.objects.using('dataTarifas').all().values_list('modalidad_extramural', flat=True).distinct().order_by('modalidad_extramural')
    # Modalidad unidad movil
    unidad_movil = reps.objects.using('dataTarifas').all().values_list('modalidad_unidad_movil', flat=True).distinct().order_by('modalidad_unidad_movil')
    # Modalidad domiciliario
    domiciliario = reps.objects.using('dataTarifas').all().values_list('modalidad_domiciliario', flat=True).distinct().order_by('modalidad_domiciliario')
    # Modalidad Jornada salud
    salud = reps.objects.using('dataTarifas').all().values_list('modalidad_jornada_salud', flat=True).distinct().order_by('modalidad_jornada_salud')
    # Modalidad prestador referencia
    mpr = reps.objects.using('dataTarifas').all().values_list('modalidad_prestador_referencia', flat=True).distinct().order_by('modalidad_prestador_referencia')
    # Modalidad prestador referencia telemedicina interactiva
    mprti = reps.objects.using('dataTarifas').all().values_list('modalidad_prestador_referencia_telemedicina_interactiva', flat=True).distinct().order_by('modalidad_prestador_referencia_telemedicina_interactiva')
    # Modalidad prestador referencia telemedicina no interactiva
    mprtni = reps.objects.using('dataTarifas').all().values_list('modalidad_prestador_referencia_telemedicina_no_interactiva', flat=True).distinct().order_by('modalidad_prestador_referencia_telemedicina_no_interactiva')
    # modalidad_prestador_referencia_tele_experticia
    mprte = reps.objects.using('dataTarifas').all().values_list('modalidad_prestador_referencia_tele_experticia', flat=True).distinct().order_by('modalidad_prestador_referencia_tele_experticia')
    # modalidad_prestador_referencia_tele_monitoreo
    mprtm = reps.objects.using('dataTarifas').all().values_list('modalidad_prestador_referencia_tele_monitoreo', flat=True).distinct().order_by('modalidad_prestador_referencia_tele_monitoreo')
    # Complejidades
    complejidades = reps.objects.using('dataTarifas').all().values_list('complejidades', flat=True).distinct().order_by('complejidades')
    
    context = {
        'registros': registros_page,
        'prestadores': data,
        'info_page': registro,
        'departamentos': dptos,
        'municipios': municipios,
        'numeros_sedes': n_sedes,
        'eses': eses,
        'serv_codigos': serv_codigos,
        'grupos': grupos,
        'intramural': intramural,
        'extramural': extramural,
        'unidad_movil': unidad_movil,
        'domiciliario': domiciliario,
        'jornada': salud,
        'mpr': mpr,
        'mprti': mprti,
        'mprtni': mprtni,
        'mprte': mprte,
        'mprtm': mprtm,
        'complejidades': complejidades,
        'filtros_aplicados': filtros_aplicados,
        'alerts': alert(proveedores),
        'vencidos': [alert for alert in alert(proveedores) if alert.dias_restantes < 0],
        'cero': [alert for alert in alert(proveedores) if alert.dias_restantes == 0],
        'uno': [alert for alert in alert(proveedores) if alert.dias_restantes == 1],
        'dos': [alert for alert in alert(proveedores) if alert.dias_restantes == 2],
        'tres': [alert for alert in alert(proveedores) if alert.dias_restantes > 2 and alert.dias_restantes < 8],
        'cuatro': [alert for alert in alert(proveedores) if alert.dias_restantes > 7 and alert.dias_restantes < 16],
        'cinco': [alert for alert in alert(proveedores) if alert.dias_restantes > 15],
        'page_title': 'REPS Data'
    }
    
    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_json = {}
        html = render_to_string('partials/pss_reps_table.html', {'prestadores': registros_page})
        data_json['html'] = html
        data_json['prestadores'] = registros_page
        data_json['data'] = data
        return JsonResponse(data_json, safe=False)

    return render(request, 'reps_data.html', context)
