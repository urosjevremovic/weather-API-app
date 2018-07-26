from rest_framework import serializers

from weather.models import City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'
        lookup_field = 'name'
        extra_kwargs = {
            'name': {'read_only': True},
            'country': {'read_only': True},
        }