# droneData/serializers.py

from rest_framework import serializers
from droneData.models import DroneData

class DroneDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroneData
        fields = '__all__'
