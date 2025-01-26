from rest_framework import serializers
from .models import Project
import googlemaps
from django.conf import settings

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def validate(self, data):
        if not data.get('latitude') or not data.get('longitude'):
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            geocode_result = gmaps.geocode(data['location'])
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                data['latitude'] = location['lat']
                data['longitude'] = location['lng']
            else:
                raise serializers.ValidationError("No se pudo validar la dirección proporcionada.")
        return data