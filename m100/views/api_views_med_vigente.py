# archivo api_views_med_vigente.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.paginator import Paginator
from ..models.models_med_vigente import m100Vigente as m100
from ..models.models_others_vigente import OthersVigente as otros
from ..models.models_med_col import m100Col as m100Colsub
from ..models.models_others_col import OthersCol as otrosColsub
from ..models.models_proveedores import proveedores as prov
from ..serializers.serializer_med_vigente import MedicamentosVigenteSerializer
from ..modules.info_actas import info_actas_medicamentos, info_actas_otros
from ..modules.estandar import obtener_datos_estandar, total_estandar
from ..modules.alert import alert
from ..modules.color_cell_alert import alert_color

class MedicamentosVigenteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MedicamentosVigenteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-fecha_pactada']
    
    # Definir todos los campos filtrables
    # filterset_fields = {
    #     'cum': ['icontains'],
    #     'expediente': ['icontains'],
    #     'descripcion_medicamento': ['icontains'],
    #     'principio_activo': ['icontains'],
    #     'concentracion': ['icontains'],
    #     'nit_proveedor': ['icontains'],
    #     'forma_farmaceutica': ['exact'],
    #     'alianza': ['exact'],
    #     'canal': ['exact'],
    #     'medicamentos_de_control_especial': ['exact'],
    #     'medicamentos_monopolio_del_estado': ['exact'],
    #     'numero_acta_inicial': ['exact'],
    #     'nombre_del_proveedor_pactado': ['exact'],
    #     'tipo': ['exact'],
    #     'novedad': ['exact'],
    #     'status': ['exact'],
    # }
    
    def get_queryset(self):
            queryset = m100.objects.all().order_by('-fecha_pactada')
            
            if not hasattr(self, 'request') or self.request is None:
                return queryset.filter(status=1)
            
            params = self.request.query_params
            print("QUERY PARAMS:", dict(params))
            
            # Filtro de status por defecto
            status = params.get('status', '1')
            if status:
                queryset = queryset.filter(status=status)
            
            # Aplicar filtros manualmente
            if params.get('cum'):
                queryset = queryset.filter(cum__icontains=params.get('cum'))
            
            if params.get('expediente'):
                queryset = queryset.filter(expediente__icontains=params.get('expediente'))
            
            if params.get('descripcion_medicamento'):
                queryset = queryset.filter(descripcion_medicamento__icontains=params.get('descripcion_medicamento'))
            
            if params.get('principio_activo'):
                queryset = queryset.filter(principio_activo__icontains=params.get('principio_activo'))
            
            if params.get('concentracion'):
                queryset = queryset.filter(concentracion__icontains=params.get('concentracion'))
            
            if params.get('nit_proveedor'):
                queryset = queryset.filter(nit_proveedor__icontains=params.get('nit_proveedor'))
            
            if params.get('forma_farmaceutica'):
                queryset = queryset.filter(forma_farmaceutica=params.get('forma_farmaceutica'))
            
            if params.get('alianza'):
                queryset = queryset.filter(alianza=params.get('alianza'))
            
            if params.get('canal'):
                queryset = queryset.filter(canal=params.get('canal'))
            
            if params.get('medicamentos_de_control_especial'):
                queryset = queryset.filter(medicamentos_de_control_especial=params.get('medicamentos_de_control_especial'))
            
            if params.get('medicamentos_monopolio_del_estado'):
                queryset = queryset.filter(medicamentos_monopolio_del_estado=params.get('medicamentos_monopolio_del_estado'))
            
            if params.get('numero_acta_inicial'):
                queryset = queryset.filter(numero_acta_inicial=params.get('numero_acta_inicial'))
            
            if params.get('nombre_del_proveedor_pactado'):
                queryset = queryset.filter(nombre_del_proveedor_pactado=params.get('nombre_del_proveedor_pactado'))
            
            if params.get('tipo'):
                queryset = queryset.filter(tipo=params.get('tipo'))
            
            if params.get('novedad'):
                queryset = queryset.filter(novedad=params.get('novedad'))
            
            # Filtro especial para regulado
            filter_regulado = params.get('valor_medicamento_regulado')
            if filter_regulado:
                if filter_regulado.lower() == 'si':
                    queryset = queryset.filter(valor_medicamento_regulado__gt='0')
                elif filter_regulado.lower() == 'no':
                    queryset = queryset.filter(valor_medicamento_regulado='0')
            
            print(f"QUERYSET FINAL COUNT: {queryset.count()}")
            
            return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Paginación
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 50)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)
        
        # Serializar los datos con color
        medicamentos_data = []
        for medicamento in page_obj:
            med_dict = MedicamentosVigenteSerializer(medicamento).data
            med_dict['color'] = alert_color(medicamento.novedad)
            medicamentos_data.append(med_dict)
        
        # Construir filtros aplicados
        filtros_aplicados = self._build_filtros_aplicados(request)
        
        return Response({
            'results': medicamentos_data,
            'pagination': {
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'current_page': page_obj.number,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            },
            'filtros_aplicados': filtros_aplicados
        })
    
    def _build_filtros_aplicados(self, request):
        """Construye la lista de filtros aplicados"""
        filtros = []
        params = request.query_params
        
        status = params.get('status', '1')
        filtros.append("Todos" if status == "" else "Activos" if status == "1" else "Inactivos")
        
        filter_mapping = {
            'cum': 'CUM',
            'expediente': 'Expediente',
            'descripcion_medicamento': 'Descripción MED',
            'principio_activo': 'Principio Activo',
            'concentracion': 'Concentración',
            'nit_proveedor': 'NIT',
            'forma_farmaceutica': 'Forma Farmacéutica',
            'alianza': 'Alianza',
            'canal': 'Canal',
            'medicamentos_de_control_especial': 'Control Especial',
            'medicamentos_monopolio_del_estado': 'Monopolio',
            'numero_acta_inicial': '#Acta o Estandar',
            'nombre_del_proveedor_pactado': 'Proveedor',
            'tipo': 'Tipo',
            'novedad': 'Novedad',
            'valor_medicamento_regulado': 'Regulado',
        }
        
        for param, label in filter_mapping.items():
            value = params.get(param)
            if value:
                filtros.append(f"{label}: {value}")
        
        return filtros
    
    @action(detail=False, methods=['get'])
    def filtros_options(self, request):
        """Endpoint para obtener las opciones de los filtros"""
        return Response({
            'formas_farmaceuticas': list(m100.objects.values_list('forma_farmaceutica', flat=True).distinct().order_by('forma_farmaceutica')),
            'alianzas': list(m100.objects.values_list('alianza', flat=True).distinct().order_by('alianza')),
            'canales': list(m100.objects.values_list('canal', flat=True).distinct().order_by('canal')),
            'control_especial': list(m100.objects.values_list('medicamentos_de_control_especial', flat=True).distinct().order_by('medicamentos_de_control_especial')),
            'monopolios': list(m100.objects.values_list('medicamentos_monopolio_del_estado', flat=True).distinct().order_by('medicamentos_monopolio_del_estado')),
            'actas': list(m100.objects.values_list('numero_acta_inicial', flat=True).distinct().order_by('numero_acta_inicial')),
            'proveedores': list(m100.objects.values_list('nombre_del_proveedor_pactado', flat=True).distinct().order_by('nombre_del_proveedor_pactado')),
            'tipos': list(m100.objects.values_list('tipo', flat=True).distinct().order_by('tipo')),
            'novedades': list(m100.objects.values_list('novedad', flat=True).distinct().order_by('novedad')),
        })
    
    @action(detail=False, methods=['get'])
    def info_complementaria(self, request):
        """Endpoint para info de actas, estandar, alertas, etc."""
        return Response({
            'info_actas_m100': info_actas_medicamentos(m100, m100Colsub),
            'info_actas_otros': info_actas_otros(otros, otrosColsub),
            'estandar': obtener_datos_estandar(m100, otros),
            'tarifario': total_estandar(m100, otros),
            'alerts': self._serialize_alerts(alert(prov)),
        })
    
    def _serialize_alerts(self, alerts):
        """Serializa las alertas agrupadas por días restantes"""
        alerts_list = list(alerts)
        return {
            'all': [self._alert_to_dict(a) for a in alerts_list],
            'vencidos': [self._alert_to_dict(a) for a in alerts_list if a.dias_restantes < 0],
            'cero': [self._alert_to_dict(a) for a in alerts_list if a.dias_restantes == 0],
            'uno': [self._alert_to_dict(a) for a in alerts_list if a.dias_restantes == 1],
            'dos': [self._alert_to_dict(a) for a in alerts_list if a.dias_restantes == 2],
            'tres': [self._alert_to_dict(a) for a in alerts_list if a.dias_restantes > 2 and a.dias_restantes < 8],
            'cuatro': [self._alert_to_dict(a) for a in alerts_list if a.dias_restantes > 7 and a.dias_restantes < 16],
            'cinco': [self._alert_to_dict(a) for a in alerts_list if a.dias_restantes > 15],
        }
    
    def _alert_to_dict(self, alert_obj):
        """Convierte objeto alert a diccionario"""
        return {
            'dias_restantes': alert_obj.dias_restantes,
            # Agrega aquí otros campos del objeto alert según tu estructura
        }