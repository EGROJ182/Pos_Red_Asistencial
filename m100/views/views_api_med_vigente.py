#archivo views_api_med_vigente
from django.shortcuts import render
from django.views import View

class MedicamentosVigenteView(View):
    """Vista que solo renderiza el template. Los datos se cargan vía API."""
    
    def get(self, request):
        context = {
            'page_title': 'HC Medicamentos Vigentes'
        }
        return render(request, 'medicamentos_vigente_api.html', context)