import os
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from dotenv import load_dotenv

import requests

from .data_for_tests import data_json_list_locations, data_json_location
from .services import LocationService


load_dotenv()
API_KEY = os.getenv('API_KEY')

# Create your tests here.

class TestLocationService(TestCase):

    @patch.object(LocationService, 'get_coordinates_locations_by_name_api')
    def test_get_coordinate_success(self, mock_get_locations):
        # изменение выходных данных функции
        mock_get_locations.return_value = data_json_list_locations

        location_service = LocationService(API_KEY)
        result = location_service.get_coordinates_locations_by_name_api('London')
        self.assertEqual(type(result), list)

        list_locations = location_service.get_coordinate('London')

        self.assertEqual(list_locations[0].name, 'London')
        self.assertEqual(list_locations[0].lon, Decimal("-0.1276"))
        self.assertEqual(list_locations[0].lat, Decimal("51.5073"))
        self.assertEqual(list_locations[0].country, "GB")

    @patch.object(LocationService, 'get_data_by_coordinates_from_api')
    def test_get_data_by_coordinates(self, mock_data):
        # изменение выходных данных функции
        mock_data.return_value = data_json_location

        location_service = LocationService(API_KEY)
        result = location_service.get_data_by_coordinates_from_api('33.33', '33, 33')
        self.assertEqual(type(result), dict)

        location = location_service.get_location_by_coordinates(1, "33.33", "33.33")

        self.assertEqual(location.id, 1)
        self.assertEqual(location.name, "Москва")
        self.assertEqual(location.temp, Decimal("-2"))
        self.assertEqual(location.feels_like, Decimal("-5"))
        self.assertEqual(location.country, "RU")
        self.assertEqual(location.icon, "01n")
        self.assertEqual(location.description, "ясно")

