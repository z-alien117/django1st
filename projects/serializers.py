from rest_framework import serializers
from .models import Project
import googlemaps
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('latitude', 'longitude',)

    def validate(self, data):
        # Validar que se proporcione la dirección
        location = data.get('location')
        if not location:
            raise serializers.ValidationError({
                "location": "El campo de ubicación es obligatorio."
            })

        try:
            # Inicializar cliente de Google Maps
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            geocode_result = gmaps.geocode(location)
            print(f"Dirección ingresada: {location}")
            print(f"Resultado de geocodificación: {geocode_result}")

            if not geocode_result:
                raise serializers.ValidationError({
                    "location": "No se pudo validar la dirección proporcionada."
                })

            # Asignar latitud y longitud
            geometry = geocode_result[0]['geometry']['location']
            data['latitude'] = geometry['lat']
            data['longitude'] = geometry['lng']

        except Exception as e:
            raise serializers.ValidationError({
                "location": f"Error al validar la dirección: {str(e)}"
            })

        return data