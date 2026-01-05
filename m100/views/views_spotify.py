from django.shortcuts import redirect
from django.http import HttpResponse

def spotify_redirect(request):
    token = request.GET.get('access_token')
    
    if token:  # Verificamos si el token está presente
        # Guarda el token en la sesión
        request.session['access_token'] = token
    else:
        # Si no hay token, puedes redirigir a una página de error o volver a iniciar sesión
        return HttpResponse("Error: No se recibió el token de acceso.", status=400)

    return redirect('home')  # Redirige a la página principal o donde necesites