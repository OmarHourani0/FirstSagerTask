import json
import threading
import paho.mqtt.client as mqtt
from .classifiers import classify
from django.utils import timezone
from django.conf import settings

DRONE_IDS = getattr(settings, 'DRONE_IDS', [])
MQTT_BROKER_URL = getattr(settings, 'MQTT_BROKER_URL', 'localhost')
MQTT_BROKER_PORT = getattr(settings, 'MQTT_BROKER_PORT', 1883)

## ASGI STUFF
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def on_new_drone_data(drone_id, data_dict):
    """
    This function sends new drone data to the WebSocket consumers.

    The function gets called whenever new drone data is received via MQTT. As soon as the data is received,
    it is converted from a dictionary to a JSON string that has two attributes the type of message being sent and the
    data itself. The data is sent both drone by drone and to all drones. Then the reciver can handle the data accordingly.

    Args:
        drone_id (ID): It is the ID of the drone for which the data will be sent, only 
                    applies when the data is only sent for that drone.
        
        data_dict (dictionary): It is the data of the drone.

    Returns:
        ReturnType: The data is sent to the websocket consumers.

    Raises:
        ExceptionType: Could raise errors if the channel layer is not set up correctly or if the data format is incorrect.
    """
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"drone_{drone_id}",
        {
            "type": "drone_data",
            "data": data_dict  # dictionary to be sent
        }
    )
    
    async_to_sync(channel_layer.group_send)(
        "drone_all",
        {
            "type": "drone_data",
            "data": {"drone_id": drone_id, **data_dict}
        }
    )
## END OF ASGI STUFF

def on_connect(client, userdata, flags, rc):
    """
    This function runs when the MQTT client connects to the broker.

    Args:
        client: The MQTT client instance.

    Returns:
        ReturnType: Does return anything but it subscribes to the topics which are the source of the drone data.

    Raises:
        ExceptionType: Will raise exceptions when the connection fails or if the topic does not exist.
    """
    
    print("Connected to MQTT broker with code:", rc)
    for drone_id in DRONE_IDS:
        topic = f"thing/product/{drone_id}/osd"
        client.subscribe(topic)
        # print(f"Subscribed to {topic}")
    print('Subscribed to topics succesfully.')

def on_message(client, userdata, msg):
    """
    The functions loads the data recieved into the DroneData model.

    When the data arrives it is recieved as a JSON string, which is then decoded and loaded into the DroneData model.
    The classification of the drone is also assigned based on the data recieved.

    Args:
        msg (JSON): It is the data recieved from the MQTT broker, as a JSON string.

    Returns:
        ReturnType: It does not return anything but it loads the data into the DroneData model.

    Raises:
        ExceptionType: Will throw exceptions if the data format is incorrect or if the database operations fail or if
        the classification function fails or if the data is not formatted in a way that can be passed to the DroneData model.
    """
    
    # print(f"[DEBUG] Raw message received on {msg.topic}: {msg.payload}")
    from .models import DroneData
    try:
        data = json.loads(msg.payload.decode())
        drone_id = msg.topic.split("/")[2]
        label = classify(data)

        DroneData.objects.update_or_create(
            drone_id=drone_id,
            defaults={
                # Position & motion
                'latitude': data['latitude'],
                'longitude': data['longitude'],
                'elevation': data['elevation'],
                'height': data['height'],
                'height_limit': data['height_limit'],
                'home_distance': data['home_distance'],
                'horizontal_speed': data['horizontal_speed'],
                'vertical_speed': data['vertical_speed'],
                'wind_speed': data['wind_speed'],
                'wind_direction': data['wind_direction'],

                # Status flags & modes
                'gear': data['gear'],
                'is_near_area_limit': bool(data['is_near_area_limit']),
                'is_near_height_limit': bool(data['is_near_height_limit']),
                'rc_lost_action': data['rc_lost_action'],
                'rid_state': bool(data['rid_state']),
                'rth_altitude': data['rth_altitude'],

                # Storage
                'storage_total': data['storage']['total'],
                'storage_used': data['storage']['used'],

                # Flight summary
                'total_flight_distance': data['total_flight_distance'],
                'total_flight_sorties': data['total_flight_sorties'],
                'total_flight_time': data['total_flight_time'],

                # Misc
                'track_id': data.get('track_id', ''),

                # Classification
                'classification': label,
            }
        )
        
        on_new_drone_data(drone_id, data)
        
        # print(f"Message received on {msg.topic}: {msg.payload.decode()}")
        # print(f"Saved data for {drone_id} at {timezone.now()}")

    except Exception as e:
        print(f"Error processing MQTT message on {msg.topic}: {e}")

     
def on_disconnect(client, userdata, rc):
    
    """
    The function closes the connection to the MQTT broker.

    Args:
        rc (flag (optional)): It is the return code of the connection.

    Returns:
        ReturnType: Does not return anything.

    Raises:
        ExceptionType: No exceptions can be raised. But it may raise one if there is no connection in the first place.
    """
    
    print("Disconnected with result code "+str(rc))


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)  # change to your broker IP/port

    thread = threading.Thread(target=client.loop_forever)
    thread.daemon = True
    thread.start()