import logging
import os
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from dotenv import load_dotenv

from locations.forms import SearchLocations
from locations.models import Location
from locations.services import LocationService

logger = logging.getLogger("locations.errors")

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
        locations_dict = {}

        for location in locations:
            cache_key = 'loc_' + str(location.id)
            current_location = cache.get(cache_key)
            if current_location:
                locations_dict[location.id] = current_location
            else:
                logger.info('обращение к API по координатам')
                current_location = location_service.get_location_by_coordinates(id_location=location.id, lat=location.latitude,
                                                                   lon=location.longitude)

                cache.set(cache_key, current_location, 120)
                locations_dict[location.id] = current_location

        return locations_dict

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

        # удаление из кеша
        if cache.get(str(location.id)):
            cache.delete(str(location.id))
        return redirect(reverse('locations:index'))


load_dotenv()
API_KEY = os.getenv('API_KEY')


class WeatherSearchView(LoginRequiredMixin, ListView):
    template_name = 'locations/search_result.html'
    model = Location
    extra_context = {
        'title': 'Страница поиска',
    }
    login_url = '/users/login/'
    redirect_field_name = ''


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
                except Exception as ex:
                    messages.error(request, message=f'Локация {location_name} уже добавлена')
                    logger.info(f"Повторное добавление локации {location_name} {ex}")
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
                messages.error(request, message=f'{locations["message"]}')
                logger.error(f'Ошибка {locations["cod"]}: {locations["message"]}')
                return redirect(reverse('locations:index'))
            return render(request, 'locations/search_result.html', self.extra_context)

class PageNotFound(TemplateView):
    template_name = 'page_404.html'
    extra_context = {
        'title': 'Страница 404',
    }