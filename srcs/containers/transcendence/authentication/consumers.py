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
        message_recu = text_data_json["message"]
        message = "beuteu"

        text_data = json.dumps({"friend_list": message})
        print(f"Message Recu: {message_recu}")

        user = self.scope['user']
        user.friends.add('neo')
        print(user.friends)
        print(user.friends.all())

        self.send(text_data)