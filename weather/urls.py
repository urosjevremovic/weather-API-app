from django.urls import path

from weather.views import CityViewSet

app_name = 'weather'
urlpatterns = [
    path('', CityViewSet.as_view(), name='posts'),
]