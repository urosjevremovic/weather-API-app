from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet

from weather.models import City
from weather.serializers import CitySerializer
from weather.service import weather_by_city_id


class CityViewSet(ModelViewSet):
    model = City
    serializer_class = CitySerializer
    queryset = City.objects.all()
    lookup_field = 'name'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context
    #     try:
    #         city_weather = weather_by_city_id(self.kwargs['pk'])['weather']
    #         print(city_weather)
    #     except KeyError:
    #         pass
    #     return context

    # def retrieve(self, request, *args, **kwargs):
    #     print(self.kwargs)
    #     return super().retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        print(type(self.kwargs['name']))
        exists = City.objects.filter(name=self.kwargs['name'])
        if not exists:
            city_weather = weather_by_city_id(self.kwargs['name'])
            print(city_weather['city_name'])
            print(city_weather['country_name'])
            city = City.objects.create(name=city_weather['city_name'], country=city_weather['country_name'])
            city.save()
        return super().retrieve(request, *args, **kwargs)


# city_weather = dict()
#     city_weather['city_name'] = data['name']
#     city_weather['country_name'] = Country.objects.get(code=data['sys']['country']).name
#     city_weather['weather'] = data['weather'][0]['main']
#     city_weather['weather_description'] = data['weather'][0]['description']
#     city_weather['temperature'] = int(round(data['main']['temp']))
#     city_weather['humidity'] = int(round(data['main']['humidity']))
#     city_weather['pressure'] = int(round(data['main']['pressure']))
#     city_weather['wind_speed'] = int(round(data['wind']['speed']))
#
# if 'deg' in data['wind']:
#     city_weather['wind_direction'] = get_wind_direction(data['wind']['deg'])
# else:
#     city_weather['wind_direction'] = 'N/A'
#
# city_weather['icon_url'] = static('weather/images/icons/{}.png'.format(data['weather'][0]['icon']))