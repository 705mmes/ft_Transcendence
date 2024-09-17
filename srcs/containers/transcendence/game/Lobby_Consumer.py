import json
from linecache import updatecache
from time import sleep
from xmlrpc.client import DateTime

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from game.models import GameLobby, TournamentLobby
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


class LobbyConsumer(WebsocketConsumer):
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
        elif mode == 'match_tournament':
            self.tournament(text_data_json)
        elif mode == 'match_ai':
            self.ai_match(text_data_json)

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
        if not self.check_lobby_existance(opponent, user):
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

# Tournament lobby

    def add_to_lobby(self, lobby, user):
        print(lobby.P1)
        print(lobby.P2)
        print(lobby.P3)
        print(lobby.P4)

    def find_3_opponent(self):
        user = User.objects.get(username=self.scope['user'])
        lobby_queryset = TournamentLobby.objects.filter(is_full=False)
        if not lobby_queryset:
            lobby = TournamentLobby.objects.create(P1=user)
        else:
            lobby = lobby_queryset.first()
            self.add_to_lobby(lobby, user)

    def searching_tournament(self):
        self.change_tournament_research(True, self.scope['user'])
        json_data = json.dumps({'action': 'searching', 'mode': 'match_tournament'})
        self.send(json_data)
        opponent_name = self.find_3_opponent()
        # if opponent_name is not None:
        #     opponent = User.objects.get(username=opponent_name)
        #     json_data = {'action': 'find_opponent', 'mode': 'matchmaking_1v1', 'opponent': opponent_name}
        #     async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
        #     json_data_2 = {'action': 'find_opponent', 'mode': 'matchmaking_1v1',
        #                    'opponent': self.scope['user'].username}
        #     async_to_sync(self.channel_layer.group_send)("game_" + opponent_name,
        #                                                  {'type': 'send_info', 'data': json_data_2})
        #     print(f"game_{opponent.username} | room name {self.room_name}")
        #     self.create_lobby(opponent_name)

    def change_tournament_research(self, new_state, username):
        user = User.objects.get(username=username)
        user.tournament_research = new_state
        user.save()

    def cancel_tournament(self):
        self.change_in_research(False, self.scope['user'])
        json_data = json.dumps({'action': 'cancel', 'mode': 'match_tournament'})
        self.send(json_data)

    def tournament(self, json_data):
        if json_data['action'] == 'searching':
            self.searching_tournament()
        elif json_data['action'] == 'cancel':
            self.cancel_tournament()
        # elif json_data['action'] == 'player_ready':
        #     self.check_player_tournament()


# AI LOBBY
    def ai_match(self, json_data):
        if json_data['action'] == 'searching':
            self.start_game_ia()

    def searching_ai(self):
        self.change_in_research(False, self.scope['user'])
        json_data = json.dumps({'action': 'find_opponent', 'mode': 'match_ai'})
        self.send(json_data)

    def start_game_ia(self):
        user = User.objects.get(username=self.scope['user'])
        self.change_in_research(False, self.scope['user'])
        self.init_ai(user)
        my_racket = self.json_creator_racket(user)
        ai_cache = cache.get(f"{user.username}_ai_key")
        ai_racket = {'up_pressed': ai_cache['up_pressed'],
                     'down_pressed': ai_cache['down_pressed'],
                     'x': ai_cache['x'],
                     'y': ai_cache['y'],
                     'score': 0,
                     'name': 'ai'}
        ball_cache = cache.get(f"{ai_cache['lobby_name']}_key")
        json_ball = {'posX': ball_cache['posX'], 'posY': ball_cache['posY'],
                     'speed': ball_cache['speed'],
                     'dirX': ball_cache['dirX'],
                     'dirY': ball_cache['dirY']}
        json_data = json.dumps({'action': 'start_game', 'mode': 'match_ai',
                                'my_racket': my_racket, 'opponent': ai_racket, 'ball': json_ball})
        self.send(json_data)

    def init_ai(self, user):
        cache.set(f"{user.username}_key", {
            'lobby_name': user.username + "_lobby_ai",
            'name': user.username,
            'x': 0,
            'y': (1080 - 233) / 2,
            'id': 1,
            'up_pressed': False, 'down_pressed': False,
            'game_loop': True
        })
        cache.set(f"{user.username}_ai_key", {
            'lobby_name': user.username + "_lobby_ai",
            'name': 'ai',
            'x': 2040 - 77,
            'y': (1080 - 233) / 2,
            'id': 2,
            'up_pressed': False, 'down_pressed': False,
            'game_loop': False
        })
        cache.set(f"{user.username}_lobby_ai_key", {
            'is_game_loop': False,
            'test': False,
            'user_key': f"{user.username}",
            'ai': f"{user.username}_ai",
            'posX': (2040 - 30) / 2,
            'posY': (1080 - 30) / 2,
            'speed': 500,
            'dirX': 500,
            'dirY': 0
        })


