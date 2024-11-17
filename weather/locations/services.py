import requests


class LocationService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_coordinate(self, location: str):
        """Получение координат по всем локациям похожим на вводимую"""
        r = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={self.api_key}')
        locations = r.json()
        processed_locations = []
        for city in locations:
            request = {
                'name': city['name'],
                "lat": city["lat"],
                "lon": city["lon"],
                "country":  city["country"],
            }
            processed_locations.append(request)
        return processed_locations

    def get_location_by_coordinates(self, lat, lon):
        """"Получение локации по координатам"""
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}')
        # print(r.json())
        return r.json()