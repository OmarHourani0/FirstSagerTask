import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    """
    The Consumer was made for testing purposes, it just returns a simple message.

    Longer description (if necessary) that explains the function in more detail,
    including any context or background.
    """
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'HELLO FROM WEBSOCKET'
        }))
    
    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"echo": text_data}))
        
class DroneTelemetryConsumer(AsyncWebsocketConsumer):
    """
    This consumer handles realitime drone data via websockets. 
    
    It receives the data and then relays it to the websocket clients. The different functions handle the connection
    and everything related to the session. It handles data for all the drones at once or for a specific 
    drone, it based on the URL parameters. When data is received, it sends an acknowledgment back.
    
    Returns:
        ReturnType: The class sends data to the WebSocket clients in JSON format.

    Raises:
        ExceptionType: Could raise errors if the connection fails or if the data format is incorrect.
    """
    async def connect(self):
        self.drone_id = self.scope['url_route']['kwargs'].get('drone_id', 'all')
        if self.drone_id == 'all':
            self.group_name = "drone_all"
        else:
            self.group_name = f"drone_{self.drone_id}"
            
        # Join group to receive broadcast messages
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        
    async def receive(self, text_data):
        # Handle incoming messages if needed
        data = json.loads(text_data)
        print(f"Received data from client:", data)
        await self.send(text_data=json.dumps({
            "type": "Response",
            "message": f"ACK from server for drone {data.get('drone_id', 'unknown')}",
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from group
    async def drone_data(self, event):
        # event["data"] is dict
        await self.send(text_data=json.dumps(event["data"]))
