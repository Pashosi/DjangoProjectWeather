import logging
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

import requests
from django.contrib import messages
from django.shortcuts import redirect
from requests import request

from locations.DTO import DTOLocationCoordinates, DTOCurrentWeatherData, DTOErrorLocation

logger = logging.getLogger("locations.errors")

class LocationService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_coordinate(self, location: str):
        """Получение координат по всем локациям похожим на вводимую"""
        locations = self.get_coordinates_locations_by_name_api(location=location)
        processed_locations = []

        if isinstance(locations, list):
            for city in locations:
                try:
                    request = DTOLocationCoordinates(
                        name=city['name'],
                        lat=Decimal(city["lat"]).quantize(Decimal('1.0000'), ROUND_DOWN),
                        lon=Decimal(city["lon"]).quantize(Decimal('1.0000'), ROUND_DOWN),
                        country=city["country"],
                        state=city["state"],
                    )
                    processed_locations.append(request)
                except KeyError as ex:
                    logger.warning(f'Пропустили город из-за ошибки в словаре. Нет ключа {ex}')
        else:
            logger.info("Вернулся не список, а словарь ошибки")
            return locations

        return processed_locations

    def get_location_by_coordinates(self, id_location: int, lat: str, lon: str):
        """"Получение локации по координатам"""
        response_api = self.get_data_by_coordinates_from_api(lat=lat, lon=lon)
        try:
            location = DTOCurrentWeatherData(
                id=id_location,
                name=response_api["name"],
                temp=Decimal(response_api["main"]["temp"]).quantize(Decimal('1'), ROUND_HALF_UP),
                feels_like=Decimal(response_api["main"]["feels_like"]).quantize(Decimal('1'), ROUND_HALF_UP),
                gust=Decimal(response_api["wind"]["speed"]).quantize(Decimal('1.0'), ROUND_HALF_UP),
                country=response_api["sys"]["country"],
                icon=response_api["weather"][0]["icon"],
                description=response_api["weather"][0]["description"],
            )
            logger.info(f'погода {response_api["weather"][0]["icon"]}')
            return location
        except Exception:
            logger.error("Не получил от API локацию")
            location = DTOErrorLocation(
                id_location=id_location,
                cod=response_api['cod'],
                error_message=response_api['message']
            )
            return location

    def get_coordinates_locations_by_name_api(self, location: str):
        """Запрос вариантов локаций с координатами по названию"""
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={self.api_key}')

        if response.ok:
            data_response = response.json()
            if len(data_response) > 0:
                return data_response
            else:
                # вариант когда ни чего не найдено, но статус 200
                return {"cod": response.status_code, "message": f'{location} не найдена'}
        else:
            # варианты 4хх и 5хх ошибок и их сообщений
            messages.error(response, message=self.get_message_error_code(response.status_code)['message'])

    def get_data_by_coordinates_from_api(self, lat: str, lon: str):
        """Запрос данных по координатам локации"""
        try:
            response = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=ru&appid={self.api_key}&units=metric')
            if response.ok:
                data_response = response.json()
                return data_response

            else:
                logger.error('другая обработка')
                # варианты 4хх и 5хх ошибок и их сообщений
                return self.get_message_error_code(response.status_code)
        except Exception as ex:
            logger.error(ex)
            return self.get_message_error_code(500)


    def get_message_error_code(self, code: int) -> dict:
        messages = {
            400: 'Неверный запрос',
            401: 'Неверный API токен',
            404: 'Неверные вводимые данные',
            429: 'Слишком много запросов',
        }
        if code in messages:
            return {"cod": code, 'message': messages[code]}
        else:
            return {
                "cod": code,
                'message': 'Непредвиденная ошибка, не связанная с правильностью данных. Пожалуйста попробуйте позже.'
            }
