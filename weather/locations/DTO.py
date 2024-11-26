from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DTOLocationCoordinates:
    name: str
    lat: Decimal
    lon: Decimal
    country: str
    state: str

    def __str__(self):
        return f'''(
            "name": {self.name},
            "lat": {self.lat},
            "lon": {self.lon},
            "country": {self.country},
            "state": {self.state}
        )'''

@dataclass
class DTOCurrentWeatherData:
    id: int
    name: str
    temp: Decimal
    feels_like: Decimal
    gust: Decimal
    country: str
    icon: str
    description: str

    def __str__(self):
        return f'''(
            'name': {self.name},
            'temp': {self.temp},
            'feels_like': {self.feels_like},
            'gust': {self.gust},
            'country': {self.country},
            'icon': {self.icon},
            'description': {self.description}
        )'''

class DTOErrorLocation:
    """Класс ошибки получения данных"""

    def __init__(self, id_location, cod, error_message):
        self.id = id_location
        self.cod = cod
        self.error_message = error_message

