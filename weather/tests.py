from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from weather.models import City
from weather.serializers import CitySerializer


class GetAllCitiesTest(APITestCase):

    def setUp(self):
        City.objects.create(
            name='Belgrade', country='RS', weather='sunny', weather_description='clear', temperature=25, humidity=30,
            pressure=40, wind_speed=5, wind_direction='NE', icon_url='http://127.0.0.1:8000/media/images/icons/01d.png',
            created=timezone.now, updated=timezone.now)
        City.objects.create(
            name='Berlin', country='DE', weather='rainy', weather_description='cloudy', temperature=25, humidity=30,
            pressure=40, wind_speed=5, wind_direction='NE', icon_url='http://127.0.0.1:8000/media/images/icons/10n.png',
            created=timezone.now, updated=timezone.now)
        City.objects.create(
            name='Madrid', country='ES', weather='rainy', weather_description='cloudy', temperature=40, humidity=30,
            pressure=40, wind_speed=5, wind_direction='NE', icon_url='http://127.0.0.1:8000/media/images/icons/10n.png',
            created=timezone.now, updated=timezone.now)

    def test_get_all_cities(self):
        response = self.client.get('http://127.0.0.1:8000/cities/')
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Belgrade', str(response.data))


class GetSingleCityTest(APITestCase):

    def setUp(self):
        self.belgrade = City.objects.create(
            name='Belgrade', country='RS', weather='sunny', weather_description='clear', temperature=25, humidity=30,
            pressure=40, wind_speed=5, wind_direction='NE', icon_url='http://127.0.0.1:8000/media/images/icons/01d.png',
            created=timezone.now, updated=timezone.now)
        self.berlin = City.objects.create(
            name='Berlin', country='DE', weather='rainy', weather_description='cloudy', temperature=25, humidity=30,
            pressure=40, wind_speed=5, wind_direction='NE', icon_url='http://127.0.0.1:8000/media/images/icons/10n.png',
            created=timezone.now, updated=timezone.now)
        self.madrid = City.objects.create(
            name='Madrid', country='ES', weather='rainy', weather_description='cloudy', temperature=40, humidity=30,
            pressure=40, wind_speed=5, wind_direction='NE', icon_url='http://127.0.0.1:8000/media/images/icons/10n.png',
            created=timezone.now, updated=timezone.now)

    def test_get_valid_single_city(self):
        response = self.client.get(f'http://127.0.0.1:8000/cities/{self.belgrade.name}/')
        city = City.objects.get(pk=self.belgrade.pk)
        serializer = CitySerializer(city)
        self.assertEqual(city.__str__(), 'Belgrade')
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_city_returns_404(self):
        response = self.client.get('http://127.0.0.1:8000/cities/Velgrade/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_retrieves_single_city_data_from_external_API(self):
        response = self.client.get('http://127.0.0.1:8000/cities/Paris/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateSingleCityTest(APITestCase):

        def setUp(self):
            self.payload = {
                'name': 'Madrid',
                'country': 'ES',
                'weather': 'rainy',
                'weather_description': 'cloudy',
                'temperature': 40,
                'humidity': 30,
                'pressure': 40,
                'wind_speed': 5,
                'wind_direction': 'NE',
                'icon_url': 'http://127.0.0.1:8000/media/images/icons/10n.png',
                'created': timezone.now,
                'updated': timezone.now,
            }

        def test_create_with_valid_data(self):
            response = self.client.post('http://127.0.0.1:8000/cities/', data=self.payload,
                                        content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)