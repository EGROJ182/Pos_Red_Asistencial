from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def happy(request):
    return render(request, 'happy-birthday-julieta.html')
