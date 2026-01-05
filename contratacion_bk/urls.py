"""
URL configuration for contratacion_bk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from m100.views.views_med_vigente import medicamentosVigente
from m100.views.views_med_homeopatica import medicamentosHomeopatica
from m100.views.views_med_antigua import medicamentosAntigua
from m100.views.views_load_data_med_vigente import loadMedVigente
from m100.views.views_load_data_med_homeopatica import loadMedHomeopatica
from m100.views.views_load_data_med_antigua import loadMedAntigua
from m100.views.views_validation_data_med_vigente import validationMedVigente
from m100.views.views_validation_data_med_antigua import validationMedAntigua
from m100.views.views_others_vigente import othersVigente
from m100.views.views_others_homeopatica import othersHomeopatica
from m100.views.views_others_antigua import othersAntigua
from m100.views.views_med_ce import MCE
from m100.views.views_med_me import MME
from m100.views.views_termometro import expTermometro
from m100.views.views_dane import data_dane
from m100.views.views_cups import cups
from m100.views.views_datos_proveedores import datosProveedores
from m100.views.views_proveedores import proveedoresContratados
from m100.views.views_reps import repsView
from m100.views.views_tablero_gerencia import dashboard
from m100.views.views_home import home
# from m100.views.views_ftp import ftp_download, ftp_browser
from m100.views.views_mft import sftp_browser, sftp_download
from m100.views.happy import happy

from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.shortcuts import redirect


from rest_framework.routers import DefaultRouter
from m100.views.api_views_med_vigente import MedicamentosVigenteViewSet
from django.views.generic import TemplateView
from m100.views.views_api_med_vigente import MedicamentosVigenteView


router = DefaultRouter()
router.register(r'medicamentos-vigente-api', MedicamentosVigenteViewSet, basename='api-medicamentos-vigente')


def custom_404(request, exception=None):
    """ Captura errores 404 y redirige automáticamente a force-404/ """
    return redirect("404")  # Usar el name de la URL

def force_404_view(request):
    """ Vista personalizada para la página 404 """
    return render(request, '404.html', status=404)

handler404 = custom_404  # Asigna el manejador de errores 404

urlpatterns = [
    path('api/', include(router.urls)),
    path('medicamentos-vigente-api/', MedicamentosVigenteView.as_view(), name='medicamentos-vigente-api'),

    path("not-found/", force_404_view, name="404"),  # Vista de error personalizada
    path("admin/", admin.site.urls),
    path("", home, name='home'),
    path("contratados/hc-vigente-medicamentos/", medicamentosVigente, name='moleculas-vigente'),
    path("contratados/hc-medicamentos-excepciones/", medicamentosHomeopatica, name='moleculas-homeopatica'),
    path("contratados/hc-antiguo-medicamentos/", medicamentosAntigua, name='moleculas-antiguo'),
    path("load-vigente/actas-medicamentos-vigente", loadMedVigente, name='load-med-vigente'),
    path("load-vigente/actas-medicamentos-excepciones", loadMedHomeopatica, name='load-med-homeopatica'),
    path("load-antigua/actas-medicamentos-antigua", loadMedAntigua, name='load-med-antiguo'),
    path("validation-vigente/medicamentos-vigente", validationMedVigente, name='validation-med-vigente'),
    path("validation-antigua/medicamentos-antigua", validationMedAntigua, name='validation-med-antiguo'),
    path("contratados/hc-vigente-otros/", othersVigente, name='otros-vigente'),
    path("contratados/hc-otros-excepciones/", othersHomeopatica, name='otros-homeopatica'),
    path("contratados/hc-antiguo-otros/", othersAntigua, name='otros-antiguo'),
    path("medicamentos/control-especial/", MCE, name='controlados'),
    path("medicamentos/monopolio-del-estado/", MME, name='monopolio'),
    path("medicamentos/termometro/", expTermometro, name='termometro'),
    path("data-dane/codigos-dane-colombia/", data_dane, name='dane'),
    path("red-positiva/cups/", cups, name='cups'),
    path("informacion-contacto-proveedores/datos/", datosProveedores, name='datos-proveedores'),
    path("proveedores-contratados/red-asistencial/", proveedoresContratados, name='proveedores'),
    path("reps-data/query/", repsView, name='reps-data'),
    path('dashboard/', dashboard, name='dashboard'),
    # Navegador SFTP
    path('mft-goanywhere/browser/', sftp_browser, name='mft_browser'),    
    # Descarga de archivos/carpetas
    path('mft/download/<str:filename>/', sftp_download, name='mft_download'),
    # path('ftp/', ftp_browser, name='ftp_browser'),
    # path('ftp/download/<str:filename>/', ftp_download, name='ftp_download'),
    # path('happy-birthday/julieta/', happy, name='happy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
