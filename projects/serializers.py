from rest_framework import serializers
from .models import Project
import googlemaps
from django.conf import settings

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('latitude', 'longitude',)  # Make these read-only since they're auto-filled

    def validate(self, data):
        # Check if location is provided
        if not data.get('location'):
            raise serializers.ValidationError({
                "location": "Location field is required"
            })

        try:
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            geocode_result = gmaps.geocode(data['location'])
            
            if not geocode_result:
                raise serializers.ValidationError({
                    "location": "Could not validate the provided address"
                })
                
            location = geocode_result[0]['geometry']['location']
            data['latitude'] = location['lat']
            data['longitude'] = location['lng']
            
        except Exception as e:
            raise serializers.ValidationError({
                "location": f"Error validating address: {str(e)}"
            })
            
        return data