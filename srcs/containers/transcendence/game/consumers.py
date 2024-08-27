import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from game.models import GameLobby, PosPlayer
from django.db.models import Q
from django.core import serializers


class GameConsumer(WebsocketConsumer):
    def connect(self):
        print(f"Connecting to game : {self.scope['user']}")
        self.room_name = "game_" + self.scope['user'].username
        print(f"room name = {self.room_name} et channel name {self.channel_name}")
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        user = User.objects.get(username=self.scope['user'])
        user.channel_name = self.channel_name
        user.save()
        PosPlayer.objects.create(Player=user)
        self.accept()

    def disconnect(self, close_code):
        user = User.objects.get(username=self.scope['user'])
        user.in_research = False
        user.is_playing = False
        user.save()
        if GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).exists():
            lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get()
            lobby.delete()
        PosPlayer.objects.get(Player=user).delete()
        print(f"Disconnecting : {self.scope['user']}")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mode = text_data_json['mode']
        if mode == 'match_1v1':
            self.match_1v1(text_data_json)
        elif mode == 'tournament':
            self.tournament(text_data_json)
        print(f"{self.scope['user']} send: {text_data_json}")

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
        elif json_data['action'] == 'get_game_data':
            self.get_game_data()
        elif json_data['action'] == 'start' or json_data['action'] == 'end':
            self.move(json_data)


    # def move_down(self, json_data):
    #     user = User.objects.get(username=self.scope['user'])
    #     if GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).exists():
    #         lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get()
    #         if lobby.Player1 == user:
    #             lobby.Player1_dir = json_data
    #             my_racket = {'x': lobby.Player1_posX, 'y': lobby.Player1_posY, 'speed': 1000}
    #             opponent_racket = {'x': lobby.Player2_posX, 'y': lobby.Player2_posY, 'speed': 1000}
    #             opponent_name = lobby.Player2.username
    #             lobby.save()
    #         else:
    #             lobby.Player2_posY -= 10
    #             my_racket = {'x': lobby.Player2_posX, 'y': lobby.Player2_posY}
    #             opponent_racket = {'x': lobby.Player1_posX, 'y': lobby.Player1_posY}
    #             opponent_name = lobby.Player1.username
    #             lobby.save()
    #         json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'my_racket': my_racket, 'opponent': opponent_racket}
    #         async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
    #         json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'opponent': my_racket, 'my_racket': opponent_racket}
    #         async_to_sync(self.channel_layer.group_send)("game_" + opponent_name, {'type': 'send_info', 'data': json_data})


    def who_is_the_enemy(self, lobby):
        if lobby.Player1 == User.objects.get(username=self.scope['user']):
            return lobby.Player2
        return lobby.Player1

    def move(self, json_data):
        user = User.objects.get(username=self.scope['user'])
        if GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).exists():
            opponent = self.who_is_the_enemy(GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get())
            user_pos = user.Player.get()
            if json_data['action'] == 'start':
                user_pos.dir = json_data['direction']
                user_pos.save()
            else:
                user_pos.dir = 'stop'
                user_pos.save()
            my_racket = {'x': user.Player.get().posX, 'y': user.Player.get().posY, 'speed': 1000, 'dir': user_pos.dir}
            opponent_racket = {'x': opponent.Player.get().posX, 'y': opponent.Player.get().posY, 'speed': 1000, 'dir': opponent.Player.get().dir}
            json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'my_racket': my_racket, 'opponent': opponent_racket}
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
            json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'my_racket': opponent_racket, 'opponent': my_racket}
            async_to_sync(self.channel_layer.group_send)("game_" + opponent.username, {'type': 'send_info', 'data': json_data})

    def get_game_data(self):
        user = User.objects.get(username=self.scope['user'])
        if GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).exists():
            lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get()
            if lobby.Player1 == user:
                print("player1 is me")
                # my_racket = {'x': lobby.Player1_posX, 'y': lobby.Player1_posY, 'speed': 1000}
                # opponent_racket = {'x': lobby.Player2_posX, 'y': lobby.Player2_posY, 'speed': 1000}
            else:
                print("player2 is me")
               #  my_racket = {'x': lobby.Player2_posX, 'y': lobby.Player2_posY}
               # opponent_racket = {'x': lobby.Player1_posX, 'y': lobby.Player1_posY}
            # json_data = {'action': 'game_data', 'mode': 'matchmaking_1v1', 'my_racket': my_racket, 'opponent': opponent_racket}
            # async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})

    def init_pos(self, lobby):
        user = User.objects.get(username=self.scope['user'])
        if lobby.Player1 == user:
            opponent_pos = lobby.Player2.Player.get()
            opponent_pos.set_to_player2()
            opponent_pos.save()
            user_pos = user.Player.get()
            user_pos.set_to_player1()
            user_pos.save()
        else:
            opponent_pos = lobby.Player1.Player.get()
            opponent_pos.set_to_player1()
            opponent_pos.save()
            user_pos = user.Player.get()
            user_pos.set_to_player2()
            user_pos.save()

    def check_player(self):
        user = User.objects.get(username=self.scope['user'])
        if GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).exists():
            self.init_pos(GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get())
            opponent = self.who_is_the_enemy(GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).get())
            if user.is_playing and opponent.is_playing:
                json_data = {'action': 'start_game', 'mode': 'matchmaking_1v1'}
                async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
                return
        print("Popo")
        json_data = {'action': 'cancel_lobby', 'mode': 'matchmaking_1v1'}
        async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})


    def tournament(self, json_data):
        pass
        # if json_data['action'] == 'searching':
            # await self.searching_tournament()
