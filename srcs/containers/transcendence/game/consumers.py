import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q
from django.core import serializers


class GameConsumer(WebsocketConsumer):
    def connect(self):
        print(f"Connecting to : {self.scope['user']}")
        self.room_name = "game_" + self.scope['user'].username
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        print(f"Disconnecting to : {self.scope['user']}")
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # action = text_data_json['action']
        # if action == 'friend_list':
            # self.send_friend_list()
        print(text_data_json)

