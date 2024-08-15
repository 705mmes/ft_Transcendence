import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from django.core import serializers


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"Connecting to game : {self.scope['user']}")
        self.room_name = "game_" + self.scope['user'].username
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print(f"Disconnecting to : {self.scope['user']}")
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        if action == 'search_match':
            await self.matchmaking()
        print(text_data_json)

    async def matchmaking(self):
        print("Matchmaking ask !")