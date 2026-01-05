import paramiko
import io
import os
import stat
import zipfile
from datetime import datetime  # 🔥 AGREGADO
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages

# Configuración SFTP
SFTP_HOST = "mft.positiva.gov.co"
SFTP_PORT = 2243
SFTP_USER = "G_medica"
SFTP_PASS = "Uhnbru0sgnpit]"

def connect_sftp():
    """Establece conexión SFTP con manejo de errores"""
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Conexión SFTP establecida.")
        return sftp, transport
    except paramiko.AuthenticationException:
        raise Exception("Error de autenticación SFTP. Verifica usuario y contraseña.")
    except paramiko.SSHException as e:
        raise Exception(f"Error SSH: {str(e)}")
    except Exception as e:
        raise Exception(f"Error de conexión SFTP: {str(e)}")

def is_directory(sftp, path):
    """Verifica si una ruta es un directorio"""
    try:
        return stat.S_ISDIR(sftp.stat(path).st_mode)
    except:
        return False

def sftp_browser(request):
    """Vista principal del navegador SFTP"""
    path = request.GET.get("path", "").strip()
    search_query = request.GET.get("search", "").strip()
    folder_filter = request.GET.get("folder", "").strip()
    file_type_filter = request.GET.get("file_type", "").strip()
    page_number = request.GET.get("page", 1)
    
    # Normalizar la ruta - NO agregar / al inicio para rutas relativas
    if path and path.endswith("/") and len(path) > 1:
        path = path[:-1]
    
    archivos = []
    carpetas = []
    error_message = None
    sftp = None
    transport = None
    
    try:
        sftp, transport = connect_sftp()
        
        # Listar items en la ruta actual
        current_path = path if path else "/"
        items = sftp.listdir(current_path)
        
        for item in items:
            try:
                item_path = f"{current_path}/{item}" if current_path != "/" else f"/{item}"
                item_stat = sftp.stat(item_path)
                
                # Determinar si es carpeta o archivo
                if stat.S_ISDIR(item_stat.st_mode):
                    carpetas.append({
                        'name': item,
                        'path': item_path,
                        'size': item_stat.st_size,
                        'modified': datetime.fromtimestamp(item_stat.st_mtime),  # 🔥 CAMBIADO: Ahora es datetime
                        # 'created': datetime.fromtimestamp(item_stat.st_atime)
                    })
                else:
                    # Obtener extensión del archivo
                    extension = os.path.splitext(item)[1].lower()
                    archivos.append({
                        'name': item,
                        'path': item_path,
                        'size': item_stat.st_size,
                        'modified': datetime.fromtimestamp(item_stat.st_mtime),  # 🔥 CAMBIADO: Ahora es datetime
                        # 'created': datetime.fromtimestamp(item_stat.st_atime),
                        'extension': extension
                    })
            except Exception as e:
                print(f"Error al procesar {item}: {e}")
                continue
        
        # Aplicar filtros
        filtros_aplicados = []
        
        if search_query:
            carpetas = [c for c in carpetas if search_query.lower() in c['name'].lower()]
            archivos = [a for a in archivos if search_query.lower() in a['name'].lower()]
            filtros_aplicados.append(f"Búsqueda: {search_query}")
        
        if folder_filter:
            carpetas = [c for c in carpetas if folder_filter.lower() in c['name'].lower()]
            filtros_aplicados.append(f"Carpeta: {folder_filter}")
        
        if file_type_filter:
            archivos = [a for a in archivos if a['extension'] == file_type_filter.lower()]
            filtros_aplicados.append(f"Extensión: {file_type_filter}")
        
        # Ordenar
        carpetas.sort(key=lambda x: x['name'])
        archivos.sort(key=lambda x: x['name'])
        
        # Obtener extensiones únicas para el filtro
        tipos = list(set([a['extension'] for a in archivos if a['extension']]))
        tipos.sort()
        
        # Calcular ruta padre
        parent_path = None
        if path:
            parent_path = "/".join(path.split("/")[:-1]) if "/" in path else ""
        
    except Exception as e:
        error_message = str(e)
        carpetas = []
        archivos = []
        tipos = []
        parent_path = None
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()
    
    # Paginación de carpetas
    carpetas_paginator = Paginator(carpetas, 50)
    carpetas_page = carpetas_paginator.get_page(page_number)
    
    # Paginación de archivos
    archivos_paginator = Paginator(archivos, 50)
    archivos_page = archivos_paginator.get_page(page_number)
    
    context = {
        'carpetas': carpetas_page,
        'archivos': archivos_page,
        'info_page': carpetas_page,  # Para compatibilidad con template
        'ruta_actual': path if path else "/",
        'parent_path': parent_path,
        'page_title': 'Explorador SFTP',
        'tipos': tipos,
        'filtros_aplicados': filtros_aplicados,
        'error_message': error_message,
    }
    
    return render(request, "mft.html", context)

def sftp_download(request, filename):
    """Descarga un archivo o carpeta del servidor SFTP"""
    path = request.GET.get("path", "").strip()
    
    # Normalizar la ruta
    if path and not path.startswith("/"):
        path = "/" + path
    
    sftp = None
    transport = None
    
    try:
        sftp, transport = connect_sftp()
        
        # Construir ruta completa del archivo
        file_path = f"{path}/{filename}" if path and path != "/" else f"/{filename}"
        
        # Verificar si es directorio o archivo
        if is_directory(sftp, file_path):
            # Descargar carpeta como ZIP
            return download_folder_as_zip(sftp, file_path, filename)
        else:
            # Descargar archivo individual
            return download_single_file(sftp, file_path, filename)
            
    except Exception as e:
        return HttpResponse(f"Error descargando: {str(e)}", status=500)
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()

def download_single_file(sftp, file_path, filename):
    """Descarga un archivo individual"""
    file_stream = io.BytesIO()
    try:
        sftp.getfo(file_path, file_stream)
        file_stream.seek(0)
        
        response = FileResponse(file_stream, as_attachment=True, filename=filename)
        return response
    except Exception as e:
        raise Exception(f"Error al descargar archivo: {str(e)}")

def download_folder_as_zip(sftp, folder_path, folder_name):
    """Descarga una carpeta completa como archivo ZIP"""
    zip_stream = io.BytesIO()
    
    try:
        with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zipf:
            add_folder_to_zip(sftp, folder_path, zipf, folder_name)
        
        zip_stream.seek(0)
        response = FileResponse(
            zip_stream, 
            as_attachment=True, 
            filename=f"{folder_name}.zip"
        )
        return response
    except Exception as e:
        raise Exception(f"Error al comprimir carpeta: {str(e)}")

def add_folder_to_zip(sftp, folder_path, zipf, arcname):
    """Agrega recursivamente archivos de una carpeta al ZIP"""
    try:
        items = sftp.listdir(folder_path)
        
        for item in items:
            item_path = f"{folder_path}/{item}"
            item_arcname = f"{arcname}/{item}"
            
            if is_directory(sftp, item_path):
                # Recursivamente agregar subcarpetas
                add_folder_to_zip(sftp, item_path, zipf, item_arcname)
            else:
                # Agregar archivo al ZIP
                file_stream = io.BytesIO()
                sftp.getfo(item_path, file_stream)
                file_stream.seek(0)
                zipf.writestr(item_arcname, file_stream.read())
    except Exception as e:
        print(f"Error al procesar {folder_path}: {e}")