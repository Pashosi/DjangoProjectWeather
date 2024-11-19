from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

import requests

from locations.DTO import DTOLocationCoordinates, DTOCurrentWeatherData


class LocationService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_coordinate(self, location: str):
        """Получение координат по всем локациям похожим на вводимую"""
        r = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={self.api_key}')
        locations = r.json()
        processed_locations = []
        for city in locations:
            request = DTOLocationCoordinates(
                name=city['name'],
                lat=Decimal(city["lat"]).quantize(Decimal('1.0000'), ROUND_DOWN),
                lon=Decimal(city["lon"]).quantize(Decimal('1.0000'), ROUND_DOWN),
                country=city["country"]
            )
            processed_locations.append(request)
        return processed_locations

    def get_location_by_coordinates(self, lat, lon):
        """"Получение локации по координатам"""
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=ru&appid={self.api_key}&units=metric')
        request = r.json()
        location = DTOCurrentWeatherData(
            name=request["name"],
            temp=Decimal(request["main"]["temp"]).quantize(Decimal('1'), ROUND_HALF_UP),
            feels_like=Decimal(request["main"]["feels_like"]).quantize(Decimal('1'), ROUND_HALF_UP),
            gust=Decimal(request["wind"]["speed"]).quantize(Decimal('1.0'), ROUND_HALF_UP),
            country=request["sys"]["country"]
        )
        return location