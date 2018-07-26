from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    weather = models.CharField(max_length=20)
    weather_description = models.CharField(max_length=40)
    temperature = models.IntegerField()
    humidity = models.PositiveIntegerField()
    pressure = models.PositiveIntegerField()
    wind_speed = models.PositiveIntegerField()
    wind_direction = models.CharField(max_length=3)
    icon_url = models.URLField()

    def __str__(self):
        return self.name
