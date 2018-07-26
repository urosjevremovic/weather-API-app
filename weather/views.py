from rest_framework.viewsets import ModelViewSet

from weather.models import City
from weather.serializers import CitySerializer


class CityViewSet(ModelViewSet):
    model = City
    serializer_class = CitySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['city_weather'] = weather_by_city_id(self.kwargs['city_id'])
        context['city_id'] = self.kwargs['city_id']
        return context
