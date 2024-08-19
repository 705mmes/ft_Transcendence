import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from django.db.models import Q
from django.core import serializers


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"Connecting to game : {self.scope['user']}")
        self.room_name = "game_" + self.scope['user'].username
        self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print(f"Disconnecting to : {self.scope['user']}")
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        if action == 'searching_opponent':
            await self.matchmaking_1v1()
        print(text_data_json)

    def get_user_in_research(self):
        print('caca')
        user_in_research = User.objects.filter(in_research=True)
        print(user_in_research)

    async def matchmaking_1v1(self):
        user = await database_sync_to_async(User.objects.get)(username=self.scope['user'])
        if user.in_research:
            user.in_research = True
        await database_sync_to_async(user.save)()
        response = {'action': 'searching_opponent', 'mode': 'matchmaking_1v1'}
        json_data = json.dumps(response)
        print(f"{self.scope['user']} is looking for game !")
        user_in_r = await sync_to_async(self.get_user_in_research)()
        print("Ici:", user_in_r)
        await self.send(json_data)
        print("ohlolo")
