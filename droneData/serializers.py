# droneData/serializers.py

from rest_framework import serializers
from droneData.models import DroneData

class DroneDataSerializer(serializers.ModelSerializer):
    """
    It is a serializer for the DronData model, it makes sure all the data is properly formatted for any and all data 
    in the DroneData model. It is used to convert the DroneData model instances into JSON format and vice versa and is used
    throughout the application.
    """
    
    class Meta:
        model = DroneData
        fields = '__all__'
