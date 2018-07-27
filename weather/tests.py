from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse

from weather.models import City
from weather.serializers import CitySerializer


class GetAllCitiesTest(TestCase):

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