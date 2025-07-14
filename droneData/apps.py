from django.apps import AppConfig
from droneData.mqtt import start_mqtt

class DronedataConfig(AppConfig):
    """
    This class defines the configuration for the droneData application.

    It has one attribute, `name`, which is the name of the application. 

    Returns:
        It has one function, `ready`, which is called when the application is ready. 
        And this function will start the MQTT client that is defined in mqqt.py 

    Raises:
        Cant raise any exceptions, but the start_mqtt() function has to be well defined in mqtt.py
        And the MQTT broker has to be running and accessible.
    """
    
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'droneData'
    verbose_name = "Drone Data"

    def ready(self):
        from droneData.mqtt import start_mqtt
        start_mqtt()
