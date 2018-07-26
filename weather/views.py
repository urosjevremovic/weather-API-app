from rest_framework.viewsets import ModelViewSet

from weather.models import City
from weather.serializers import CitySerializer
from weather.service import weather_by_city_id


class CityViewSet(ModelViewSet):
    model = City
    serializer_class = CitySerializer
    queryset = City.objects.all()
    lookup_field = 'name'
    http_method_names = ['get', ]

    def retrieve(self, request, *args, **kwargs):
        self.kwargs['name'] = self.kwargs['name'].capitalize()
        exists = City.objects.filter(name=self.kwargs['name'])
        print(exists)
        if not exists:
            city_weather = weather_by_city_id(self.kwargs['name'])
            city = City.objects.create(name=city_weather['city_name'], country=city_weather['country_name'],
                                       weather=city_weather['weather'],
                                       weather_description=city_weather['weather_description'],
                                       temperature=city_weather['temperature'], humidity=city_weather['humidity'],
                                       pressure=city_weather['pressure'], wind_speed=city_weather['wind_speed'],
                                       wind_direction=city_weather['wind_direction'], icon_url=city_weather['icon_url'])
            city.save()
        return super().retrieve(request, *args, **kwargs)
