from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def weather_checker(request):
    data = {
        'title': 'Страница поиска локаций',
    }
    return render(request, 'locations/index.html', context=data)