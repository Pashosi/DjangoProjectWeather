from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DTOLocationCoordinates:
    name: str
    lat: Decimal
    lon: Decimal
    country: str

    def __str__(self):
        return f'''(
            "name": {self.name},
            "lat": {self.lat},
            "lon": {self.lon},
            "country": {self.country},
        )'''

@dataclass
class DTOCurrentWeatherData:
    name: str
    temp: Decimal
    feels_like: Decimal
    gust: Decimal
    country: str

    def __str__(self):
        return f'''(
            'name': {self.name},
            'temp': {self.temp},
            'feels_like': {self.feels_like},
            'gust': {self.gust},
            'country': {self.country},
        )'''
