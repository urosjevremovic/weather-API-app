import os
import requests

from django.contrib.sites.shortcuts import get_current_site

from weather.utils import get_wind_direction

API_KEY = os.environ.get('WEATHER_API_KEY')


def weather_by_city_name(request, city_name):
    """Takes weather from Weather API and returns it."""

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    data = requests.get(url.format(city_name, API_KEY)).json()
    if len(data) < 5:
        return ''

    city_weather = dict()
    city_weather['city_name'] = data['name']
    city_weather['country_name'] = data['sys']['country']
    city_weather['weather'] = data['weather'][0]['main']
    city_weather['weather_description'] = data['weather'][0]['description']
    city_weather['temperature'] = int(round(data['main']['temp']))
    city_weather['humidity'] = int(round(data['main']['humidity']))
    city_weather['pressure'] = int(round(data['main']['pressure']))
    city_weather['wind_speed'] = int(round(data['wind']['speed']))

    if 'deg' in data['wind']:
        city_weather['wind_direction'] = get_wind_direction(data['wind']['deg'])
    else:
        city_weather['wind_direction'] = 'N/A'

    city_weather['icon_url'] = ''.join(['http://', get_current_site(request).domain,
                                        '/media/images/icons/{}.png'.format(data['weather'][0]['icon'])])

    return city_weather
