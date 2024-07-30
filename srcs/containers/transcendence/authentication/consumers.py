import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User


class ActiveConsumer(WebsocketConsumer):
    def connect(self):

        print(f"Connecting to : {self.scope['user'].username}")

        self.accept()
        self.scope['user'].is_connected = True
        self.scope['user'].save()
        # print(f"Accepted WebSocket connection from {self.scope['user']}")

    def disconnect(self, close_code):
        # Leave room group
        self.scope['user'].is_connected = False
        self.scope['user'].save()
        # print(f"Disconnecting social socket: {self.scope['user']}")

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message_recu = text_data_json["message"]
        action = text_data_json["action"]
        if action == 'friend_list_pls':
            text_data = json.dumps({"friend_list": "Leon"})
        #   Friend_list.get(self.scope['user'])

        print(f"Message Recu: {action}")

        self.send(text_data)