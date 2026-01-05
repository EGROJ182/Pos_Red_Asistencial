from urllib.parse import unquote
from ftplib import FTP_TLS
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse
import os
import io
from django.urls import path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Configuración FTP
FTP_HOST = "190.26.216.110"
FTP_PORT = 990
FTP_USER = "ftp_Redasistencial"
FTP_PASS = "@eik7N$2e#5E5W"

def connect_ftp():
    ftps = FTP_TLS()
    ftps.connect(FTP_HOST, FTP_PORT)
    ftps.login(FTP_USER, FTP_PASS)
    ftps.prot_p()  # Modo seguro
    return ftps

def ftp_browser(request):
    path = request.GET.get("path", "")
    # page = request.GET.get("page")
    search_query = request.GET.get("search", "")
    file_type = request.GET.get("file_type", "")
    folder_filter = request.GET.get("folder", "")

    ftps = connect_ftp()
    try:
        ftps.cwd(path)
    except Exception:
        path = ""
        ftps.cwd(path)
    
    archivos = []
    carpetas = []
    extenciones = set()
    
    for item in ftps.nlst():
        try:
            ftps.cwd(item)
            carpetas.append(item)
            ftps.cwd("..")
        except Exception:
            archivos.append(item)
            # extraer la extencion
            extension = os.path.splitext(item)[1]
            if extension not in extenciones:
                extenciones.add(extension)
    
    filtros_aplicados = []

    # Filtrar archivos y carpetas
    if search_query:
        archivos = [archivo for archivo in archivos if search_query.lower() in archivo.lower()]
        carpetas = [carpeta for carpeta in carpetas if search_query.lower() in carpeta.lower()]
        filtros_aplicados.append(f"Búsqueda por Query: {search_query}")
    
    if file_type:
        archivos = [archivo for archivo in archivos if archivo.endswith(file_type)]
        filtros_aplicados.append(f"Búsqueda por Tipo de Archivo: {file_type}")
    
    if folder_filter:
        carpetas = [carpeta for carpeta in carpetas if folder_filter.lower() in carpeta.lower()]
        filtros_aplicados.append(f"Búsqueda por Carpeta: {folder_filter}")
    
    # Paginación
    # paginator = Paginator(archivos, 20)
    paginatorArchivos = Paginator(archivos, 20)
    pageNumberArchivos = request.GET.get('page')
    archivos_page = paginatorArchivos.get_page(pageNumberArchivos)
    
    paginatorCarpetas = Paginator(carpetas, 30)
    pageNumberCarpetas = request.GET.get('page')
    carpetas_page = paginatorCarpetas.get_page(pageNumberCarpetas)
    
    # try:
    #     archivos_page = paginator.page(page)
    # except PageNotAnInteger:
    #     archivos_page = paginator.page(1)
    # except EmptyPage:
    #     archivos_page = paginator.page(paginator.num_pages)
    
    ftps.quit()
    
    parent_path = "/".join(path.split("/")[:-1]) if path else ""

    context = {
        "archivos": archivos_page,
        "carpetas": carpetas_page,
        "ruta_actual": path,
        "parent_path": parent_path,
        "info_page": carpetas_page,
        "filtros_aplicados": filtros_aplicados,
       "tipos": sorted(list(extenciones)),
        "title": "FTP Browser"
    }

    # Rendirizar solo la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/ftp_table_carpetas.html', {"archivos": archivos_page,
        "carpetas": carpetas_page,
        "ruta_actual": path,
        "parent_path": parent_path,
        "info_page": carpetas_page,
        "filtros_aplicados": filtros_aplicados})
        html2 = render_to_string('partials/ftp_table_archivos.html', {"archivos": archivos_page,
        "carpetas": carpetas_page,
        "ruta_actual": path,
        "parent_path": parent_path,
        "info_page": carpetas_page,
        "filtros_aplicados": filtros_aplicados})
        return JsonResponse({'html': html, 'html2': html2})

    return render(request, "ftp.html", context)


def ftp_download(request, filename):
    path = request.GET.get("path", "")
    filename = unquote(filename)  # 🔄 Decodifica caracteres URL
    remote_path = f"{path}/{filename}".strip("/")

    ftps = connect_ftp()
    file_stream = io.BytesIO()

    try:
        ftps.retrbinary(f"RETR {remote_path}", file_stream.write)
    except Exception as e:
        print(f"Error descargando {remote_path}: {e}")
        return HttpResponse("Error descargando el archivo", status=500)
    
    file_stream.seek(0)
    ftps.quit()
    
    return FileResponse(file_stream, as_attachment=True, filename=filename)


def ftp_download(request, filename):
    path = request.GET.get("path", "")
    ftps = connect_ftp()
    file_stream = io.BytesIO()
    ftps.retrbinary(f"RETR {path}/{filename}", file_stream.write)
    file_stream.seek(0)
    ftps.quit()
    return FileResponse(file_stream, as_attachment=True, filename=filename)