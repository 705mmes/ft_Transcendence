import json
from linecache import updatecache
from time import sleep
from xmlrpc.client import DateTime

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from game.models import GameLobby
from django.db.models import Q
from datetime import datetime
import math
import time
import asyncio
import redis
from django.core import serializers
from django.core.cache import cache
from time import process_time
from game.PlayerClass import Player
from game.BallClass import Ball



class GameConsumer(WebsocketConsumer):
    def connect(self):
        print(f"Connecting to game : {self.scope['user']}")
        self.room_name = "game_" + self.scope['user'].username
        print(f"room name = {self.room_name} et channel name {self.channel_name}")
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        user = User.objects.get(username=self.scope['user'])
        user.channel_name = self.channel_name
        user.save()
        self.accept()

    def disconnect(self, close_code):
        user = User.objects.get(username=self.scope['user'])
        user.in_research = False
        user.save()
        if GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).exists():
            lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get()
            # opponent = self.who_is_the_enemy(lobby)
            print("Lobby delete :", cache.get((f"{lobby.Name}_key")))
            lobby.delete()
        print(f"Disconnecting : {self.scope['user']}")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mode = text_data_json['mode']
        print(f"{self.scope['user']} send: {text_data_json}")
        if mode == 'match_1v1':
            self.match_1v1(text_data_json)
        elif mode == 'tournament':
            self.tournament(text_data_json)

    def find_opponent(self):
        user = User.objects.get(username=self.scope['user'])
        queryset = User.objects.filter(in_research=True).exclude(id=user.id).order_by('id')
        opponent = queryset.first()
        if opponent:
            print(f"Opponent found: {opponent.username}")
            return opponent.username
        else:
            print("No opponent found")
            return None

    def change_in_research(self, new_state, username):
        user = User.objects.get(username=username)
        user.in_research = new_state
        user.save()

    def change_is_playing(self, new_state, username):
        user = User.objects.get(username=username)
        user.is_playing = new_state
        user.save()

    def send_info(self, event):
        data = event['data']
        # print(json.dumps(data, indent=1))
        self.send(text_data=json.dumps(data))

    def check_lobby_existance(self, opponent, user):
        # Convert the synchronous ORM call to an async operation
        exists = GameLobby.objects.filter(
            (Q(Player1=user) & Q(Player2=opponent)) | (Q(Player1=opponent) & Q(Player2=user))).exists()
        return exists

    def create_lobby(self, opponent_name):
        opponent = User.objects.get(username=opponent_name)
        user = User.objects.get(username=self.scope['user'])
        self.change_in_research(False, opponent.username)
        self.change_in_research(False, user)
        self.change_is_playing(True, opponent.username)
        self.change_is_playing(True, user)
        if self.check_lobby_existance(opponent, user) == False:
            lobby = GameLobby.objects.create(Player1=user, Player2=opponent,
                                             Name=f"{user.username}_{opponent.username}")
            async_to_sync(self.channel_layer.group_add)(lobby.Name, user.channel_name)
            async_to_sync(self.channel_layer.group_add)(lobby.Name, opponent.channel_name)

    def searching_1v1(self):
        self.change_in_research(True, self.scope['user'])
        json_data = json.dumps({'action': 'searching', 'mode': 'match_1v1'})
        self.send(json_data)
        opponent_name = self.find_opponent()
        if opponent_name is not None:
            opponent = User.objects.get(username=opponent_name)
            json_data = {'action': 'find_opponent', 'mode': 'matchmaking_1v1', 'opponent': opponent_name}
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
            json_data_2 = {'action': 'find_opponent', 'mode': 'matchmaking_1v1',
                           'opponent': self.scope['user'].username}
            async_to_sync(self.channel_layer.group_send)("game_" + opponent_name,
                                                         {'type': 'send_info', 'data': json_data_2})
            print(f"game_{opponent.username} | room name {self.room_name}")
            self.create_lobby(opponent_name)

    def cancel_1v1(self):
        self.change_in_research(False, self.scope['user'])
        json_data = json.dumps({'action': 'cancel', 'mode': 'match_1v1'})
        self.send(json_data)

    def match_1v1(self, json_data):
        if json_data['action'] == 'searching':
            self.searching_1v1()
        elif json_data['action'] == 'cancel':
            self.cancel_1v1()
        elif json_data['action'] == 'player_ready':
            self.check_player()

    def who_is_the_enemy(self, lobby):
        if lobby.Player1 == User.objects.get(username=self.scope['user']):
            return lobby.Player2
        return lobby.Player1

    def set_player(self, player1, player2, lobby_name):
        cache.set(f"{player1.username}_key", {
            'lobby_name': lobby_name,
            'name': player1.username,
            'x': 0,
            'y': (1080 - 233) / 2,
            'id': 1,
            'up_pressed': False, 'down_pressed': False,
            'game_loop': True
        })
        cache.set(f"{player2.username}_key", {
            'lobby_name': lobby_name,
            'name': player2.username,
            'x': 2040 - 77,
            'y': (1080 - 233) / 2,
            'id': 2,
            'up_pressed': False, 'down_pressed': False,
            'game_loop': False
        })


    def init_pos(self, lobby):
        user = User.objects.get(username=self.scope['user'])
        opponent = self.who_is_the_enemy(lobby)
        if lobby.Player1 == user:
            self.set_player(user, opponent, lobby.Name)
        else:
            self.set_player(opponent, user, lobby.Name)
        print(lobby.Name)
        cache.set(f"{lobby.Name}_key", {
            'is_game_loop': False,
            'test': False,
            'user_key': f"{user.username}",
            'opponent_key': f"{opponent.username}",
            'posX': (2040 - 30) / 2,
            'posY': (1080 - 30) / 2,
            'speed': 500,
            'dirX': 500,
            'dirY': 0
        })

    def json_creator_racket(self, user):
        user_cache = cache.get(f"{user.username}_key")
        racket = {'up_pressed': user_cache['up_pressed'],
                  'down_pressed': user_cache['down_pressed'],
                  'x': user_cache['x'],
                  'y': user_cache['y'],
                  'score': 0,
                  'name': user.username,
                  }
        return racket

    def json_creator_ball(self, lobby):
        ball_cache = cache.get(f"{lobby.Name}_key")
        ball = {'posX': ball_cache['posX'], 'posY': ball_cache['posY'],
                'speed': ball_cache['speed'],
                'dirX': ball_cache['dirX'],
                'dirY': ball_cache['dirY']
                }
        return ball

    def check_player(self):
        user = User.objects.get(username=self.scope['user'])
        lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user))
        if lobby:
            self.init_pos(lobby.first())
            opponent = self.who_is_the_enemy(lobby.get())
            if user.is_playing and opponent.is_playing:
                my_racket = self.json_creator_racket(user)
                opponent_racket = self.json_creator_racket(opponent)
                json_ball = self.json_creator_ball(lobby.first())
                json_data = {'action': 'start_game', 'mode': 'matchmaking_1v1', 'my_racket': my_racket,
                             'opponent': opponent_racket, 'ball': json_ball}
                async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
                json_data_2 = {'action': 'start_game', 'mode': 'matchmaking_1v1', 'my_racket': opponent_racket,
                             'opponent': my_racket, 'ball': json_ball}
                async_to_sync(self.channel_layer.group_send)("game_" + opponent.username, {'type': 'send_info', 'data': json_data_2})
                return
        json_data = {'action': 'cancel_lobby', 'mode': 'matchmaking_1v1'}
        async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
        return

    def tournament(self, json_data):
        pass
        # if json_data['action'] == 'searching':
        # await self.searching_tournament()


class AsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "match_" + self.scope['user'].username
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        user_cache = await sync_to_async(cache.get)(f"{self.scope['user'].username}_key")
        lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
        opponent_cache = await sync_to_async(cache.get)(f"{self.who_is_the_enemy(lobby_cache)}_key")
        self.user = Player(user_cache['id'], user_cache['name'])
        self.opponent = Player(opponent_cache['id'], opponent_cache['name'])
        self.ball = Ball()
        print(f"Consumer of {self.scope['user']} state game loop : {lobby_cache['is_game_loop']}")
        if user_cache['game_loop'] and not lobby_cache['is_game_loop']:
            lobby_cache['is_game_loop'] = True
            await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)
            caca = asyncio.create_task(self.game_loop(lobby_cache))
        print(user_cache.get('lobby_name'))
        await self.accept()

    async def disconnect(self, code):
        user_name = self.scope['user'].username
        user = await sync_to_async(User.objects.get)(username=user_name)
        user.is_playing = False
        await sync_to_async(user.save)()
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print(f"Disconnected from match : {self.scope['user'].username}")
        if await sync_to_async(cache.get)(f"{user_name}_key"):
            user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
            lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
            opponent_name = self.who_is_the_enemy(lobby_cache)
            lobby_cache['is_game_loop'] = False
            await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)
            opponent = await sync_to_async(User.objects.get)(username=user_name)
            if opponent.is_playing:
                json_data = {'action': 'game_end', 'mode': 'matchmaking_1v1'}
                await self.channel_layer.group_send("match_" + opponent_name, {'type': 'send_match_info', 'data': json_data})


    # UTILS HERE
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        print(f"{self.scope['user']} send: {text_data_json}")
        if text_data_json['action'] == 'move':
            await self.update_cache(text_data_json)


    async def send_match_info(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def ft_sleep(self, delay):
        now = time.time()
        while (time.time() < now + delay):
            continue

    async def check_move(self, user_cache, opponent_cache):
        if user_cache['up_pressed'] != self.user.up_pressed or user_cache['down_pressed'] != self.user.down_pressed:
            self.user.up_pressed = user_cache['up_pressed']
            self.user.down_pressed = user_cache['down_pressed']
            return False
        elif opponent_cache['up_pressed'] != self.opponent.up_pressed or opponent_cache['down_pressed'] != self.opponent.down_pressed:
            self.opponent.up_pressed = opponent_cache['up_pressed']
            self.opponent.down_pressed = opponent_cache['down_pressed']
            return False
        return True

    def who_is_the_enemy(self, lobby_cache):
        if self.scope['user'].username == lobby_cache['user_key']:
            return lobby_cache['opponent_key']
        else:
            return lobby_cache['user_key']

    async def json_creator_racket(self, user):
        user_cache = await sync_to_async(cache.get)(f"{user.name}_key")
        racket = {'x': user.x, 'y': user.y ,
                  'up_pressed': user_cache['up_pressed'],
                  'down_pressed': user_cache['down_pressed'],
                  'score': user.score}
        return racket

    async def json_creator_ball(self):
        ball = {'posX': self.ball.x , 'posY': self.ball.y,
                'dirX': self.ball.dirX,
                'dirY': self.ball.dirY
                }
        return ball

    # GAME LOGIQUE HERE

    async def game_loop(self, lobby_cache):
        user_name = self.scope['user'].username
        while lobby_cache['is_game_loop']:
            t1 = time.perf_counter()
            user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
            opponent_cache = await sync_to_async(cache.get)(f"{self.who_is_the_enemy(lobby_cache)}_key")
            lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
            await self.ball.move(self.user.get_class(), self.opponent.get_class())
            await self.check_move(user_cache, opponent_cache)
            self.user.move(user_cache['up_pressed'], user_cache['down_pressed'])
            self.opponent.move(opponent_cache['up_pressed'], opponent_cache['down_pressed'])
            await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_data')
            await self.send_data(self.opponent.get_class(), self.user.get_class(), 'game_data')
            if await self.check_game(self.user.get_class(), self.opponent.get_class()):
                break
            await self.ft_sleep(max(0.0, 0.01667 - (time.perf_counter() - t1)))
        print(f"Consumer of {user_name}, in {user_cache['lobby_name']} Game STOPED !")
        await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_end')
        await self.send_data(self.opponent.get_class(), self.user.get_class(), 'game_end')
        await sync_to_async(cache.delete)(f"{lobby_cache['opponent_key']}_key")
        await sync_to_async(cache.delete)(f"{user_cache['lobby_name']}_key")
        await sync_to_async(cache.delete)(f"{user_name}_key")

    async def check_game(self, user, opponent):
        if user.score >= 5:
            return True
        elif opponent.score >= 5:
            return True
        return False
    #     if a player disconnect Return true

    async def update_cache(self, json_data):
        user_name = self.scope['user'].username
        user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
        user_cache['up_pressed'] = json_data['racket']['up_pressed']
        user_cache['down_pressed'] = json_data['racket']['down_pressed']
        print(f"move up: {user_cache['up_pressed']}, move down: {user_cache['down_pressed']}")
        await sync_to_async(cache.set)(f"{user_name}_key", user_cache)

    async def send_data(self, player1, player2, action):
        user_json = await self.json_creator_racket(player1)
        opponent_json = await self.json_creator_racket(player2)
        ball_json = await self.json_creator_ball()
        json_data = {'action': action, 'mode': 'matchmaking_1v1', 'my_racket': user_json,
                     'opponent': opponent_json, 'ball': ball_json}
        await self.channel_layer.group_send("match_" + player1.name, {'type': 'send_match_info', 'data': json_data})
