# Ref: https://channels.readthedocs.io/en/latest/tutorial/index.html
from channels.generic.websocket import AsyncWebsocketConsumer
import json

''' When a user posts a message, a JavaScript function will transmit the message over WebSocket to a ChatConsumer. 
The ChatConsumer will receive that message and forward it to the group corresponding to the room name. 
Every ChatConsumer in the same group (and thus in the same room) will then receive the message from the 
group and forward it over WebSocket back to JavaScript, where it will be appended to the chat log.'''

class DashboardConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.group_name = 'Dashboard'
        return super().__init__(*args, **kwargs)

    async def connect(self):
        # If WebSocket tries to connect:

        # Adding this consumer's channel to the group:
        await self.channel_layer.group_add(self.group_name,
                                            self.channel_name)
        # Accepting connection:
        await self.accept()

    async def disconnect(self, close_code):
        # If WebSocket disconnected:

        # Removing channel from group:
        await self.channel_layer.group_discard(self.group_name,
                                                self.channel_name)

    async def receive(self, text_data):                     # When altered name of 'text_data', application broke.
    # Receiving data from WebSocket:

        data_dict = json.loads(text_data)                   # Loading data from JSON to a dictionary.

        #person_name = data_dict_received['person_name']    # Getting only 'person_name'.

        #data_dict_to_be_sent = {
        #        'type': 'send_data',                       # Name of method to be used.
        #        'person_name': person_name
        #    }

        data_dict['type'] = 'send_data'                     # Adding one field to dictionary, with the name of the method to be used.

        # Broadcasting data to all channels in group:
        await self.channel_layer.group_send(self.group_name, 
                                            data_dict)

    async def send_data(self, event):
    # Sending to the (one) connected WebSocket:

        # Building JSON to be sent:
        data_JSON = json.dumps(event) # Obs: 'data_JSON' was 'text_data'. Change did not brake application.

        # Sending JSON to WebSocket:
        await self.send(data_JSON)