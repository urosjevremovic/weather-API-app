import json
import os

import requests
from django.templatetags.static import static

from weather.models import Country


API_KEY = os.environ.get('WEATHER_API_KEY')


def weather_by_city_id(city_id):
    """Takes weather from Weather API and returns it."""

    url = 'http://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric'
    try:
        response = requests.get(url.format(city_id, API_KEY)).json()
    except:
        pass

    data = json.loads(response)

    city_weather = dict()
    city_weather['city_name'] = data['name']
    city_weather['country_name'] = Country.objects.get(code=data['sys']['country']).name
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

    city_weather['icon_url'] = static('weather/images/icons/{}.png'.format(data['weather'][0]['icon']))

    return city_weather


def get_wind_direction(degree):
    """Convert wind degree to direction."""

    DEGREES = [-11.25, 11.25, 33.75, 56.25,
               78.75, 101.25, 123.75, 146.25,
               168.75, 191.25, 213.75, 236.25,
               258.75, 281.25, 303.75, 326.25, 348.75]

    DIRECTIONS = ['N', 'NNE', 'NE', 'ENE',
                  'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW',
                  'W', 'WNW', 'NW', 'NNW']

    # North wind correction.
    if degree > 348.75:
        degree -= 360

    for i in range(len(DIRECTIONS)):
        left_border = DEGREES[i]
        right_border = DEGREES[i + 1]

        if left_border < degree <= right_border:
            return DIRECTIONS[i]
