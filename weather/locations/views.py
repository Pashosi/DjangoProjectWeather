import os
from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from dotenv import load_dotenv

from locations.forms import SearchLocations
from locations.models import Location
from locations.services import LocationService


class WeatherHome(ListView):
    template_name = 'locations/index.html'
    model = Location
    context_object_name = 'cities'
    extra_context = {
        'title': 'Главная страница',
    }

    def get_queryset(self):
        locations = Location.objects.filter(user_id_id=self.request.user.id)

        location_service = LocationService(API_KEY)
        list_data_locations = []

        for location in locations:
            loc = location_service.get_location_by_coordinates(id_location=location.id, lat=location.latitude,
                                                               lon=location.longitude)
            if not isinstance(loc, dict):
                list_data_locations.append(loc)
            else:
                messages.error(self.request, message='ошибка при получении данных')
        return list_data_locations

    def get_context_data(self, *, object_list=None, **kwargs):
        # добавление формы в контекст
        context = super().get_context_data(**kwargs)
        context.update({'form': SearchLocations()})
        return context

    def post(self, request, *args, **kwargs):
        # обработка удаления карточки
        location_id = self.request.POST.get('id')

        location = Location.objects.get(id=location_id)
        location.delete()
        return redirect(reverse('locations:index'))


load_dotenv()
API_KEY = os.getenv('API_KEY')


class WeatherSearchView(ListView):
    template_name = 'locations/search_result.html'
    model = Location
    extra_context = {
        'title': 'Страница поиска',
    }

    def post(self, request, *args, **kwargs):
        method = self.request.POST.get("method_post")

        # добавление локации
        if method == "add_post":
            # Получаем координаты из POST запроса
            location_name = request.POST.get('name')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            if location_name and latitude and longitude:
                try:
                    if self.request.user.id:
                        Location.objects.create(
                            name=location_name,
                            user_id=self.request.user,
                            latitude=Decimal(latitude.replace(',', '.')),
                            longitude=Decimal(longitude.replace(',', '.')),
                        )
                except Exception:
                    messages.error(request, message=f'ошибка повторного добавления локации {location_name}')
            return redirect(reverse('locations:index'))

        # пост запрос формы поиска локаций
        else:
            location = self.request.POST.get('city')  # Получаем параметр "city" из POST запроса

            # получение списка локаций с координатами
            location_service = LocationService(API_KEY)
            locations = location_service.get_coordinate(location)

            # добавление списка в контекст
            if isinstance(locations, list):
                self.extra_context['cities'] = locations
            else:
                self.extra_context['errors'] = locations
            return render(request, 'locations/search_result.html', self.extra_context)
