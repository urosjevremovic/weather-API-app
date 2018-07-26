from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=255)


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
