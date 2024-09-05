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
import asyncio
from django.core import serializers
from django.core.cache import cache


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
        user.is_playing = False
        user.save()
        if GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).exists():
            lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get()
            opponent = self.who_is_the_enemy(lobby)
            print(cache.get((f"{lobby.Name}_key")))
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
        elif json_data['action'] == 'move':
            self.move(json_data)
        elif json_data['action'] == 'ball_info':
            user = self.scope['user']
            lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).first()
            if lobby:
                self.calcul_pos_ball(lobby.Name, json_data['racket'])  # Racket c'est la ball enfaite
                # self.ball_info(lobby, json_data['racket'])


    # async def game_loop(self):
    #     while (1):
    #         print("caca")
    #         sleep(0.016)

    def who_is_the_enemy(self, lobby):
        if lobby.Player1 == User.objects.get(username=self.scope['user']):
            return lobby.Player2
        return lobby.Player1

    # def reset_ball(self, ball_cache):
    #     ball_cache['speed'] = 500
    #     ball_cache['posX'] = 2040 / 2 - 15
    #     ball_cache['posY'] = 1080 / 2 - 15
    #     if ball_cache['dirX'] < 0:
    #         ball_cache['dirX'] = ball_cache['speed']
    #     else:
    #         ball_cache['dirX'] = -ball_cache['speed']
    #     ball_cache['dirY'] = 0
    #     return ball_cache
    #
    # # def ball_info(self, lobby, json_data):
    # #     ball_cache = cache.get(lobby.Name + "_key")
    # #     json_data = {'action': 'ball_data', 'mode': 'matchmaking_1v1', 'ball': ball_cache}
    # #     # async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
    # #     async_to_sync(self.channel_layer.group_send)("game_" + ball_cache['opponent'], {'type': 'send_info', 'data': json_data})
    #
    # def change_dirY(self, ball_cache, ball_radius):
    #     ball_cache['dirY'] *= -1
    #     if ball_cache['posY'] > 1080 - ball_radius:
    #         ball_cache['posY'] = 1080 - ball_radius
    #     elif ball_cache['posY'] < 0:
    #         ball_cache['posY'] = 0
    #     print("dirY changed !")
    #     return ball_cache

    def calcul_pos_ball(self, lobby_name, ball):
        ball_cache = cache.get(lobby_name + "_key")
        ball_cache['posX'] = ball['x']
        ball_cache['posY'] = ball['y']
        ball_cache['dirX'] = ball['dirx']
        ball_cache['dirY'] = ball['diry']
        print(json.dumps(ball_cache, indent=1))  # Pour un print joli
        json_data = {'action': 'ball_data', 'mode': 'matchmaking_1v1', 'ball': ball_cache}
        async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
        async_to_sync(self.channel_layer.group_send)("game_" + ball_cache['opponent'],
                                                     {'type': 'send_info', 'data': json_data})
        cache.set(lobby_name + "_key", ball_cache)

    # def calcul_pos_ball(self, lobby_name, client_ball):
    #     ball_cache = cache.get(lobby_name + "_key")
    #     actual_time = datetime.now().timestamp()
    #     av_dt = 16
    #     ball_radius = 30
    #     #print(f"actual time :{actual_time}")
    #     time_passed = actual_time - ball_cache['update_time']
    #     #print(f"time_passed = {time_passed}")
    #     dx = ball_cache['dirX'] * time_passed
    #     dy = ((time_passed * 1000) / av_dt) * (ball_cache['dirY'])
    #     ball_cache['posX'] += dx
    #     ball_cache['posY'] += dy
    #     print(f"dx ={dx} et dy = {dy}")
    #     print(f"posx ={ball_cache['posX']} et posy = {ball_cache['posY']}")
    #     ball_cache = self.hit_me(ball_cache, ball_radius)
    #     if ball_cache['posY'] > 1080 - ball_radius or ball_cache['posY'] < ball_radius:
    #         ball_cache = self.change_dirY(ball_cache, ball_radius)
    #     if ball_cache['posX'] > 2040 or ball_cache['posX'] < 0 + ball_radius:
    #         ball_cache = self.reset_ball(ball_cache)
    #     ball_cache['update_time'] = actual_time
    #     print(f"new_dirX {ball_cache['dirX']}, new_dirY {ball_cache['dirY']}")
    #     # print(json.dumps(ball_cache, indent=1))
    #     cache.set(lobby_name + "_key", ball_cache)
    #     json_data = {'action': 'ball_data', 'mode': 'matchmaking_1v1', 'ball': ball_cache}
    #     async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
    #     async_to_sync(self.channel_layer.group_send)("game_" + ball_cache['opponent'],
    #                                                  {'type': 'send_info', 'data': json_data})
    #
    # def hit_me(self, ball_cache, ball_radius):
    #     user_cache = cache.get(f"{self.scope['user']}_key")
    #     if user_cache['posX'] == 0:
    #         if (ball_cache['posX'] - ball_radius < user_cache['posX'] + 37
    #                 and (ball_cache['posY'] + ball_radius > user_cache['posY']
    #                      and ball_cache['posY'] - ball_radius < user_cache['posY'] + 223)):
    #             ball_cache['dirX'] *= -1
    #             if (ball_cache['dirX'] > 0 and ball_cache['speed'] * 4 > ball_cache['dirX']
    #                     or ball_cache['dirX'] < 0 and ball_cache['speed'] * 4 > ball_cache['dirX'] * -1):
    #                 ball_cache['dirX'] *= 1.1
    #             # ball_cache['posX'] = 100 + ball_radius
    #             ball_cache['dirY'] += self.impact(ball_cache, user_cache) * 7
    #     else:
    #         if (ball_cache['posX'] + ball_radius > user_cache['posX'] + 64
    #                 and (ball_cache['posY'] + ball_radius > user_cache['posY']
    #                      and ball_cache['posY'] - ball_radius < user_cache['posY'] + 223)):
    #             ball_cache['dirX'] *= -1
    #             if (ball_cache['dirX'] > 0 and ball_cache['speed'] * 4 > ball_cache['dirX']
    #                     or ball_cache['dirX'] < 0 and ball_cache['speed'] * 4 > ball_cache['dirX'] * -1):
    #                 ball_cache['dirX'] *= 1.1
    #             # ball_cache['posX'] = 2040 - 100 - 30
    #             ball_cache['dirY'] += self.impact(ball_cache, user_cache) * 7
    #     return ball_cache
    #
    # def impact(self, ball_cache, user_cache):
    #     impact = (ball_cache['posY'] - user_cache['posY']) - (223 / 2)
    #     normal = (impact / (223 / 2))
    #     print("normal :", normal)
    #     return normal

    def calcul_pos_racket(self, user_key):
        user_cache = cache.get(user_key)
        start = user_cache.get('time_start')
        end = user_cache.get('time_end')
        server_input_time = math.ceil((end - start) * 1000)
        average_dt = 16
        move = int((server_input_time * 60 / 1000)) * average_dt
        if user_cache['up_pressed']:
            if user_cache['posY'] > 0:
                user_cache['posY'] -= move
                if user_cache['posY'] < 0:
                    user_cache['posY'] = 0
        elif user_cache['down_pressed']:
            if user_cache['posY'] < 847:
                user_cache['posY'] += move
                if user_cache['posY'] > 847:
                    user_cache['posY'] = 847
        user_cache['time_start'] = 0
        user_cache['time_end'] = 0
        cache.set(user_key, user_cache)

    def update_cache(self, json_data, user):
        user_key = f"{user.username}_key"
        old_cache = cache.get(user_key)
        updated_cache = {
            'posX': old_cache['posX'],
            'posY': json_data['racket']['y'],
            'up_pressed': json_data['racket']['up_pressed'],
            'down_pressed': json_data['racket']['down_pressed'],
            'time_end': old_cache['time_end'],
            'time_start': old_cache['time_start'],
        }
        if updated_cache['up_pressed'] and updated_cache['down_pressed'] and old_cache['time_start'] != 0:
            updated_cache['time_end'] = datetime.now().timestamp()
        else:
            if (updated_cache['up_pressed'] or updated_cache['down_pressed']) and old_cache['time_start'] == 0:
                updated_cache['time_start'] = datetime.now().timestamp()
            elif not updated_cache['up_pressed'] and old_cache['up_pressed'] and old_cache['time_end'] == 0:
                updated_cache['time_end'] = datetime.now().timestamp()
            elif not updated_cache['down_pressed'] and old_cache['down_pressed'] and old_cache['time_end'] == 0:
                updated_cache['time_end'] = datetime.now().timestamp()
        cache.set(user_key, updated_cache)

    def move(self, json_data):
        user = User.objects.get(username=self.scope['user'])
        lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user))
        if lobby.exists():
            self.update_cache(json_data, user)
            opponent = self.who_is_the_enemy(lobby.get())
            user_cache = cache.get(f"{user.username}_key")
            if user_cache.get('time_end') != 0:
                self.calcul_pos_racket(f"{user.username}_key")
            my_racket = self.json_creator_racket(user)
            opponent_racket = self.json_creator_racket(opponent)
            # print(json.dumps(game_ball, indent=1)) # Pour un print joli
            json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'my_racket': my_racket,
                         'opponent': opponent_racket}  # J'ai enlever ball
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
            json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'my_racket': opponent_racket,
                         'opponent': my_racket}  # J'ai enlever ball
            async_to_sync(self.channel_layer.group_send)("game_" + opponent.username,
                                                         {'type': 'send_info', 'data': json_data})

    def set_player(self, player1, player2, lobby_name):
        cache.set(f"{player1.username}_key", {
            'lobby_name': lobby_name,
            'posX': 0, 'posY': 1080 / 2 - 233 / 2,
            'up_pressed': False, 'down_pressed': False,
            'time_start': 0, 'time_end': 0
        })
        cache.set(f"{player2.username}_key", {
            'lobby_name': lobby_name,
            'posX': 2040 - 77, 'posY': 1080 / 2 - 233 / 2,
            'up_pressed': False, 'down_pressed': False,
            'time_start': 0, 'time_end': 0
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
            'user_key': f"{user.username}",
            'opponent_key': f"{opponent.username}"
        })

    def json_creator_racket(self, user):
        user_cache = cache.get(f"{user.username}_key")
        racket = {'x': user_cache['posX'], 'y': user_cache['posY'], 'speed': 1000,
                  'up_pressed': user_cache['up_pressed'],
                  'down_pressed': user_cache['down_pressed']}
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
                #game_ball = self.json_creator_ball(lobby.first())
                # print(json.dumps(game_ball, indent=1))
                json_data = {'action': 'start_game', 'mode': 'matchmaking_1v1', 'my_racket': my_racket,
                             'opponent': opponent_racket}
                async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
                async_to_sync(self.channel_layer.group_send)("game_" + opponent.username, {'type': 'send_info', 'data': json_data})
                return 0
        json_data = {'action': 'cancel_lobby', 'mode': 'matchmaking_1v1'}
        async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
        return 1
    def tournament(self, json_data):
        pass
        # if json_data['action'] == 'searching':
        # await self.searching_tournament()


class AsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "match_" + self.scope['user'].username
        user = await sync_to_async(User.objects.get)(username=self.scope['user'])
        print(user.username)
        user_cache = await sync_to_async(cache.get)(f"{user.username}_key")
        lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
        opponent_cache = await sync_to_async(cache.get)(f"{lobby_cache['opponent_key']}_key")
        if not lobby_cache['is_game_loop']:
            caca = asyncio.create_task(self.game_loop(lobby_cache))
        print(user_cache.get('lobby_name'))

        await self.accept()

    async def game_loop(self, lobby_cache):
        user_name = self.scope['user']
        lobby_cache['is_game_loop'] = True
        opponent_cache = await sync_to_async(cache.get)(f"{lobby_cache['opponent_key']}_key")
        user_cache = await sync_to_async(cache.get)(f"{lobby_cache['user_key']}_key")
        await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)
        while lobby_cache['is_game_loop']:
            print(user_cache['lobby_name'], lobby_cache['is_game_loop'])
            lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
            await asyncio.sleep(2)
        cache.delete(f"{lobby_cache['opponent_key']}_key")
        cache.delete(f"{user_cache['lobby_name']}_key")
        cache.delete(f"{user_name}_key")

    async def disconnect(self, code):
        user_name = self.scope['user']
        print(f"Disconnected from match : {self.scope['user']}")
        if await sync_to_async(cache.get)(f"{user_name}_key"):
            user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
            lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
            opponent_name = lobby_cache['opponent_key']
            lobby_cache['is_game_loop'] = False
            await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)
            json_data = {'action': 'stop_game', 'mode': 'matchmaking_1v1'}
            await self.channel_layer.group_send("match_" + opponent_name, {'type': 'send_info', 'data': json_data})