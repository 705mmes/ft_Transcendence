import json
from linecache import updatecache
from time import sleep
from xmlrpc.client import DateTime

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from game.models import GameLobby
from django.db.models import Q
from datetime import datetime
import math
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
            cache.delete(f"{opponent.username}_key")
            cache.delete(f"{user.username}_key")
            cache.delete(f"{lobby.Name}_key")
            print(cache.get((f"{user.username}_key")))
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
            lobby = GameLobby.objects.create(Player1=user, Player2=opponent, Name=f"{user.username}_{opponent.username}")
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
            json_data_2 = {'action': 'find_opponent', 'mode': 'matchmaking_1v1', 'opponent': self.scope['user'].username}
            async_to_sync(self.channel_layer.group_send)("game_" + opponent_name, {'type': 'send_info', 'data': json_data_2})
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
            self.calcul_pos_ball(GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get().Name)


    def who_is_the_enemy(self, lobby):
        if lobby.Player1 == User.objects.get(username=self.scope['user']):
            return lobby.Player2
        return lobby.Player1

    def reset_ball(self, ball_cache):
        ball_cache['posX'] = 2040 / 2 - 15
        ball_cache['posY'] = 1080 / 2 - 15
        ball_cache['dirX'] = ball_cache['dirX'] * -1
        ball_cache['dirY'] = 0
        ball_cache['speed'] = 500

    def calcul_pos_ball(self, lobby_name):
        ball_cache = cache.get(lobby_name + "_key")
        actual_time = datetime.now().timestamp()
        av_dt = 16
        ball_radius = 30
        print(f"actual time :{actual_time}")

        time_passed = actual_time - ball_cache['update_time']
        print(f"time_passed = {time_passed}")
        dx = ((time_passed * 1000) / av_dt) * (ball_cache['dirX'] / 60)
        dy = ((time_passed * 1000) / av_dt) * (ball_cache['dirY'] / 60)
        ball_cache['posX'] += dx
        ball_cache['posY'] += dy
        print(f"dx ={dx} et dy = {dy}")
        if ball_cache['posX'] > 2040 or ball_cache['posX'] < 0 - ball_radius:
            self.reset_ball(ball_cache)
        if ball_cache['posY'] > 1080 or ball_cache['posY'] < 0 - ball_radius:
            ball_cache['posY'] *= -1
        ball_cache['update_time'] = actual_time
        # print(f"new_posX {old_ball_cache['posX'] }, new_posY {old_ball_cache['posY']}")
        print(json.dumps(ball_cache, indent=1))
        cache.set(lobby_name + "_key", ball_cache)
        json_data = {'action': 'ball_data', 'mode': 'matchmaking_1v1', 'ball': ball_cache}
        async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})

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
            # self.calcul_pos_ball(lobby.get().Name)
            my_racket = self.json_creator_racket(user)
            opponent_racket = self.json_creator_racket(opponent)
            # game_ball = self.json_creator_ball(lobby.get()) # La ball vient d'ici
            # print(json.dumps(game_ball, indent=1)) # Pour un print joli
            json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'my_racket': my_racket, 'opponent': opponent_racket} # J'ai enlever ball
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
            json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'my_racket': opponent_racket, 'opponent': my_racket} # J'ai enlever ball
            async_to_sync(self.channel_layer.group_send)("game_" + opponent.username, {'type': 'send_info', 'data': json_data})

    def set_player(self, player1, player2):
        cache.set(f"{player1.username}_key", {
            'posX': 0, 'posY': 1080 / 2 - 233 / 2,
            'up_pressed': False, 'down_pressed': False,
            'time_start': 0, 'time_end': 0
        })
        cache.set(f"{player2.username}_key", {
            'posX': 2040 - 77, 'posY': 1080 / 2 - 233 / 2,
            'up_pressed': False, 'down_pressed': False,
            'time_start': 0, 'time_end': 0
        })

    def init_pos(self, lobby):
        user = User.objects.get(username=self.scope['user'])
        opponent = self.who_is_the_enemy(lobby)
        if lobby.Player1 == user:
            self.set_player(user, opponent)
        else:
            self.set_player(opponent, user)
        print(lobby.Name)
        cache.set(f"{lobby.Name}_key", {
            'posX': 2040 / 2 - 15, 'posY':1080 / 2 - 15,
            'dirX': -500, 'dirY': 0, 'speed': 500,
            'update_time': datetime.now().timestamp()
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
        if lobby.exists():
            self.init_pos(lobby.get())
            opponent = self.who_is_the_enemy(lobby.get())
            if user.is_playing and opponent.is_playing:
                my_racket = self.json_creator_racket(user)
                opponent_racket = self.json_creator_racket(opponent)
                game_ball = self.json_creator_ball(lobby.get())
                print(json.dumps(game_ball, indent=1))
                json_data = {'action': 'start_game', 'mode': 'matchmaking_1v1', 'my_racket': my_racket,
                             'opponent': opponent_racket, 'ball': game_ball}
                async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
                return
        json_data = {'action': 'cancel_lobby', 'mode': 'matchmaking_1v1'}
        async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})


    def tournament(self, json_data):
        pass
        # if json_data['action'] == 'searching':
            # await self.searching_tournament()
