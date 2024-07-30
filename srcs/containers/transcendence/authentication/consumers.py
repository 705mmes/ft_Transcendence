import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, FriendList
from django.core import serializers


class ActiveConsumer(WebsocketConsumer):
    def connect(self):

        print(f"Connecting to : {self.scope['user']}")

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
        user = self.scope['user']
        text_data_json = json.loads(text_data)
        # message_recu = text_data_json["message"]
        action = text_data_json["action"]
        if action == 'friend_list_stp':
            text_data = json.dumps({"action": "friend_list", "friend": "Leon", "pending": "Arthur", "request": "dilo"})
        if action == 'show_all_users':
            test = FriendList.objects.all()
            print(test)
            # my_friends = FriendList
            # all_user = User.objects.all()
            # users_value = User.values('username', 'is_connected')
            # text_data = serializers.serialize('json', users_value)
            print(text_data)


        print(f"Message Recu: {action}")

        self.send(text_data)