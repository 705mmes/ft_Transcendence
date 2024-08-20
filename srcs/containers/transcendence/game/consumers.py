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
        print(f"room name = {self.room_name}")
        await self.channel_layer.group_add(self.room_name, self.channel_name)
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

    async def find_opponent(self):
        user = await User.objects.aget(username=self.scope['user'])
        queryset = User.objects.filter(in_research=True).exclude(id=user.id).order_by('id')
        opponent = await queryset.afirst()
        if opponent:
            print(f"Opponent found: {opponent.username}")
            return opponent.username
        else:
            print("No opponent found")
            return None

    async def change_in_research(self, new_state):
        user = await User.objects.aget(username=self.scope['user'])
        user.in_research = new_state
        await user.asave()
        json_data = json.dumps({'action': 'searching_opponent', 'mode': 'matchmaking_1v1'})
        await self.send(json_data)
        # print(f"send {json_data}")

    async def send_info(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def matchmaking_1v1(self):
        await self.change_in_research(True)
        opponent_name = await self.find_opponent()
        if opponent_name is not None:
            opponent = await User.objects.aget(username=opponent_name)
            json_data = json.dumps({'action': 'find_opponent', 'mode': 'matchmaking_1v1', 'opponent': opponent_name})
            await self.send(json_data)
            json_data_2 = json.dumps({'action': 'find_opponent', 'mode': 'matchmaking_1v1', 'opponent': self.scope['user'].username})
            await self.channel_layer.group_send("game_" + opponent.username, {'type': 'send_info', 'data': json_data_2})
            print(f"game_{opponent.username} | room name {self.room_name}")
            # print(f"send {json_data}")
        else:
            return