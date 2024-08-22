import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from game.models import GameLobby
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
        user = await User.objects.aget(username=self.scope['user'])
        user.in_research = False
        user.is_playing = False
        await user.asave()
        print(f"Disconnecting : {self.scope['user']}")
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mode = text_data_json['mode']
        if mode == 'match_1v1':
            await self.match_1v1(text_data_json)
        elif mode == 'tournament':
            await self.tournament(text_data_json)
        print(f"{self.scope['user']} send: {text_data_json}")

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

    async def change_in_research(self, new_state, username):
        user = await User.objects.aget(username=username)
        user.in_research = new_state
        await user.asave()

    async def change_is_playing(self, new_state, username):
        user = await User.objects.aget(username=username)
        user.is_playing = new_state
        await user.asave()
        # json_data = json.dumps({'action': 'searching', 'mode': 'match_1v1'})
        # await self.send(json_data)

    async def send_info(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def check_lobby_existance(self, opponent, user):
        # Convert the synchronous ORM call to an async operation
        exists = await sync_to_async(GameLobby.objects.filter(
            (Q(Player1=user) & Q(Player2=opponent)) | (Q(Player1=opponent) & Q(Player2=user))).exists)()
        return exists

    async def create_lobby(self, opponent_name):
        opponent = await User.objects.aget(username=opponent_name)
        user = await User.objects.aget(username=self.scope['user'])
        await self.change_in_research(False, opponent.username)
        await self.change_in_research(False, user)
        await self.change_is_playing(True, opponent.username)
        await self.change_is_playing(True, user)
        if await self.check_lobby_existance(opponent, user) == False:
            await sync_to_async(GameLobby.objects.create)(Player1=user, Player2=opponent)

    async def searching_1v1(self):
        await self.change_in_research(True, self.scope['user'])
        json_data = json.dumps({'action': 'searching', 'mode': 'match_1v1'})
        await self.send(json_data)
        opponent_name = await self.find_opponent()
        if opponent_name is not None:
            opponent = await User.objects.aget(username=opponent_name)
            json_data = {'action': 'find_opponent', 'mode': 'matchmaking_1v1', 'opponent': opponent_name}
            await self.channel_layer.group_send(self.room_name, {'type': 'send_info', 'data': json_data})
            json_data_2 = {'action': 'find_opponent', 'mode': 'matchmaking_1v1', 'opponent': self.scope['user'].username}
            await self.channel_layer.group_send("game_" + opponent.username, {'type': 'send_info', 'data': json_data_2})
            print(f"game_{opponent.username} | room name {self.room_name}")
            await self.create_lobby(opponent_name)
        else:
            return

    async def cancel_1v1(self):
        await self.change_in_research(False, self.scope['user'])
        json_data = json.dumps({'action': 'cancel', 'mode': 'match_1v1'})
        await self.send(json_data)

    async def match_1v1(self, json_data):
        if json_data['action'] == 'searching':
            await self.searching_1v1()
        elif json_data['action'] == 'cancel':
            await self.cancel_1v1()
        elif json_data['action'] == 'player_ready':
            await self.check_player()

    async def check_player(self):
        pass
        # user = User.objects.aget(self.scope['user'])
        # queryset = await sync_to_async(GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get)()


    async def tournament(self, json_data):
        pass
        # if json_data['action'] == 'searching':
            # await self.searching_tournament()
