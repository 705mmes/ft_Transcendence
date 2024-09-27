import json
from linecache import updatecache
from time import sleep
from xmlrpc.client import DateTime

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from game.models import GameLobby, GameHistory
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

class GameConsumer(AsyncWebsocketConsumer):

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
            opponent_name = self.opponent.name
            if lobby_cache:
                lobby_cache['is_game_loop'] = False
                await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)
            opponent = await sync_to_async(User.objects.get)(username=opponent_name)
            if opponent.is_playing:
                await self.check_game(self.user.get_class(), self.opponent.get_class(), True)
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
        while time.time() < (now + delay):
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
        self.start_time = time.time()
        while lobby_cache['is_game_loop']:
            t1 = time.perf_counter()
            user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
            opponent_cache = await sync_to_async(cache.get)(f"{self.who_is_the_enemy(lobby_cache)}_key")
            lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
            ball_move = await self.ball.move(self.user.get_class(), self.opponent.get_class())
            racket_move = await self.check_move(user_cache, opponent_cache)
            self.user.move(user_cache['up_pressed'], user_cache['down_pressed'])
            self.opponent.move(opponent_cache['up_pressed'], opponent_cache['down_pressed'])
            if not racket_move or ball_move:
                print("Send message to client !")
                await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_data')
                await self.send_data(self.opponent.get_class(), self.user.get_class(), 'game_data')
            if await self.check_game(self.user.get_class(), self.opponent.get_class(), False):
                break
            await self.ft_sleep(max(0.0, 0.01667 - (time.perf_counter() - t1)))
        print(f"Consumer of {user_name}, in {user_cache['lobby_name']} Game STOPED !")
        await self.send_data(self.opponent.get_class(), self.user.get_class(), 'game_end')
        await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_end')
        await sync_to_async(cache.delete)(f"{lobby_cache['opponent_key']}_key")
        await sync_to_async(cache.delete)(f"{user_cache['lobby_name']}_key")
        await sync_to_async(cache.delete)(f"{user_name}_key")

    async def check_game(self, user, opponent, ff):
        if user.score >= 5 or opponent.score >= 5:
            self.endtime = time.time() - self.start_time
            user_user = await sync_to_async(User.objects.get)(username=user.name)
            opponent_user = await sync_to_async(User.objects.get)(username=opponent.name)
            await sync_to_async(GameHistory.objects.create)(History1=user_user, History2=opponent_user,
                                                            Score1=self.user.score, Score2=self.opponent.score,
                                                            ffed1=False, ffed2=False,
                                                            date=datetime.now().strftime("%Y-%m-%d"),
                                                            minutes=self.endtime / 60, seconds=self.endtime % 60)
            return True
        else:
            if ff:
                print("la")
                self.endtime = time.time() - self.start_time
                user_user = await sync_to_async(User.objects.get)(username=user.name)
                opponent_user = await sync_to_async(User.objects.get)(username=opponent.name)
                await sync_to_async(GameHistory.objects.create)(History1=user_user, History2=opponent_user,
                                                                Score1=self.user.score, Score2=self.opponent.score,
                                                                ffed1=True, ffed2=False,
                                                                date=datetime.now().strftime("%Y-%m-%d"),
                                                                minutes=self.endtime / 60, seconds=self.endtime % 60)
            return False

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