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

class GameAIConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "match_" + self.scope['user'].username
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        user_cache = await sync_to_async(cache.get)(f"{self.scope['user'].username}_key")
        lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
        opponent_cache = await sync_to_async(cache.get)(f"{lobby_cache['ai']}_key")
        self.user = Player(user_cache['id'], user_cache['name'])
        self.opponent = Player(opponent_cache['id'], opponent_cache['name'])
        self.ball = Ball()
        if user_cache['game_loop'] and not lobby_cache['is_game_loop']:
            lobby_cache['is_game_loop'] = True
            await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)
            caca = asyncio.create_task(self.game_loop(lobby_cache))
        # print(user_cache.get('lobby_name'))
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
            if lobby_cache:
                lobby_cache['is_game_loop'] = False
                await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)


#utils

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        # print(f"{self.scope['user']} send: {text_data_json}")
        if text_data_json['action'] == 'move':
            await self.update_cache(text_data_json)


    async def send_match_info(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def ft_sleep(self, delay):
        now = time.time()
        while time.time() < (now + delay):
            continue



# game

    async def check_move(self, user_cache):
        if user_cache['up_pressed'] != self.user.up_pressed or user_cache['down_pressed'] != self.user.down_pressed:
            self.user.up_pressed = user_cache['up_pressed']
            self.user.down_pressed = user_cache['down_pressed']
            return False
        return True


    async def json_creator_racket(self, user):
        user_cache = await sync_to_async(cache.get)(f"{user.name}_key")
        racket = {'x': user.x, 'y': user.y,
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
        ia_time = time.time()
        while lobby_cache['is_game_loop']:
            t1 = time.perf_counter()
            user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
            lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
            opponent_cache = await sync_to_async(cache.get)(f"{lobby_cache['ai']}_key")
            if time.time() - ia_time > 1:
                # print('caca')
                ia_time = time.time()
                self.ball.ia_ball_snapshot()
                if self.ball.ia_dirX < 0:
                    self.ball.ia_y = (1080 / 2) - 111.5
                else:
                    await self.tracking_ai()
            await self.ball.move(self.user.get_class(), self.opponent.get_class())
            await self.check_move(user_cache)
            await self.up_down_ai()
            self.user.move(user_cache['up_pressed'], user_cache['down_pressed'])
            self.opponent.move(self.opponent.up_pressed, self.opponent.down_pressed)
            await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_data')
            if await self.check_game(self.user.get_class(), self.opponent.get_class()):
                break
            await self.ft_sleep(max(0.0, 0.01667 - (time.perf_counter() - t1)))
        await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_end')
        await sync_to_async(cache.delete)(f"{lobby_cache['ai']}_key")
        await sync_to_async(cache.delete)(f"{user_cache['lobby_name']}_key")
        await sync_to_async(cache.delete)(f"{user_name}_key")

    async def check_game(self, user, opponent):
        if user.score >= 5 or opponent.score >= 5:
            user = await sync_to_async(User.objects.get)(username=user.name)
            await sync_to_async(GameHistory.objects.create)(History1=user, History2=None,
                                                            Score1=self.user.score, Score2=self.opponent.score)
            return True
        return False
    #     if a player disconnect Return true

    async def update_cache(self, json_data):
        user_name = self.scope['user'].username
        user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
        user_cache['up_pressed'] = json_data['racket']['up_pressed']
        user_cache['down_pressed'] = json_data['racket']['down_pressed']
        await sync_to_async(cache.set)(f"{user_name}_key", user_cache)

    async def send_data(self, player1, player2, action):
        user_json = await self.json_creator_racket(player1)
        opponent_json = {'up_pressed': self.opponent.up_pressed,
                         'down_pressed': self.opponent.down_pressed,
                         'x': self.opponent.x,
                         'y': self.opponent.y,
                         'score': self.opponent.score,
                         'name': 'ai'}
        ball_json = await self.json_creator_ball()
        json_data = {'action': action, 'mode': 'match_ai', 'my_racket': user_json,
                     'opponent': opponent_json, 'ball': ball_json}
        await self.channel_layer.group_send("match_" + player1.name, {'type': 'send_match_info', 'data': json_data})

# AI GAMEPLAY

    async def up_down_ai(self):
        if  self.opponent.y > self.ball.ia_y:
            self.opponent.down_pressed = False
            self.opponent.up_pressed = True
        elif self.opponent.y + 223 < self.ball.ia_y:
            self.opponent.down_pressed = True
            self.opponent.up_pressed = False
        else:
            #print("stopped")
            self.opponent.up_pressed = False
            self.opponent.down_pressed = False
        # print("ai posy = ", self.opponent.y, "ai posy extreme = ", self.opponent.y + 223, "ball snapshot = ", self.ball.ia_y)


    async def tracking_ai(self):
        # if self.ball.ia_x + ((self.ball.ia_dirX * 0.01667) * 60) > 2040:
        #     diff = self.ball.ia_x + ((self.ball.ia_dirX * 0.01667) * 60) - 2040
        #     after_hit = 60 - (diff / self.ball.ia_dirX)
        #     before_hit = 60 - after_hit
        #     self.ball.ia_y += self.ball.ia_dirY * before_hit
        #     print("x axis ai calibrating")
        if self.ball.ia_y + (self.ball.ia_dirY * 60) > 1080 or self.ball.ia_y + (self.ball.ia_y * 60) < 0:
            if self.ball.ia_dirY > 0:
                diff = self.ball.ia_y + (self.ball.ia_dirY * 60) - 1080
            else:
                diff = self.ball.ia_y + (self.ball.ia_dirY * 60)
            after_hit = 60 - (diff / self.ball.ia_dirY)
            before_hit = 60 - after_hit
            self.ball.ia_y += self.ball.ia_dirY * before_hit
            self.ball.ia_dirY *= -1
            self.ball.ia_y += self.ball.ia_dirY * after_hit
            print("y axis ai calibrating")
        else:
            self.ball.ia_y += self.ball.ia_dirY * 60
            print("no axis ai calibrating")
        print("ai goes to = ", self.ball.ia_y)



        # elif self.ball.ia_x + (self.ball.ia_dirX * 60) > 2040:
        #     self.ball.ia_y += self.ball.ia_dirY * (60 - ((self.ball.ia_y + (self.ball.ia_dirY * 60) - 2040) / self.ball.ia_dirX))