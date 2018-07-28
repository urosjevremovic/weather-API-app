from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from weather.models import City
from weather.serializers import CitySerializer
from weather.service import weather_by_city_name


class CityViewSet(ModelViewSet):
    model = City
    serializer_class = CitySerializer
    queryset = City.objects.all()
    lookup_field = 'name'
    http_method_names = ['get', ]

    def retrieve(self, request, *args, **kwargs):
        self.kwargs['name'] = self.kwargs['name'].title()
        exists = City.objects.filter(name=self.kwargs['name'])
        if exists:
            city = exists.first()
            if (timezone.now() - city.created).seconds > 3600 and (timezone.now() - city.updated).seconds > 3600:
                city_weather = weather_by_city_name(request, self.kwargs['name'])
                City.objects.filter(name=city.name).update(name=city_weather['city_name'],
                                                           country=city_weather['country_name'],
                                                           weather=city_weather['weather'],
                                                           weather_description=city_weather['weather_description'],
                                                           temperature=city_weather['temperature'],
                                                           humidity=city_weather['humidity'],
                                                           pressure=city_weather['pressure'],
                                                           wind_speed=city_weather['wind_speed'],
                                                           wind_direction=city_weather['wind_direction'],
                                                           icon_url=city_weather['icon_url'])
                city.refresh_from_db()
        else:
            city_weather = weather_by_city_name(request, self.kwargs['name'])
            if city_weather:
                city = City.objects.create(name=city_weather['city_name'], country=city_weather['country_name'],
                                           weather=city_weather['weather'],
                                           weather_description=city_weather['weather_description'],
                                           temperature=city_weather['temperature'], humidity=city_weather['humidity'],
                                           pressure=city_weather['pressure'], wind_speed=city_weather['wind_speed'],
                                           wind_direction=city_weather['wind_direction'],
                                           icon_url=city_weather['icon_url'])
                city.save()
            else:
                pass
        return super().retrieve(request, *args, **kwargs)
