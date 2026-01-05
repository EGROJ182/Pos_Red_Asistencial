# serializers.py (en tu app de medicamentos)
from rest_framework import serializers
from ..models.models_med_vigente import m100Vigente as m100

class MedicamentosVigenteSerializer(serializers.ModelSerializer):
    # Campo calculado para el color
    color = serializers.SerializerMethodField()
    
    class Meta:
        model = m100
        fields = '__all__'
    
    def get_color(self, obj):
        from ..modules.color_cell_alert import alert_color
        return alert_color(obj.novedad)