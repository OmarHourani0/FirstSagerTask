from django.apps import AppConfig
from droneData.mqtt_client import start_mqtt

class DronedataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'droneData'

    def ready(self):
        start_mqtt()
