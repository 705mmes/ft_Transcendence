import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, FriendList, FriendRequest
from django.db.models import Q
from django.core import serializers


class ActiveConsumer(WebsocketConsumer):
    def connect(self):

        print(f"Connecting to : {self.scope['user']}")

        self.accept()
        self.scope['user'].is_connected = True
        self.scope['user'].save()
        # print(f"Accepted WebSocket connection from {self.scope['user']}")

    def disconnect(self, close_code):
        # Leave room group
        self.scope['user'].is_connected = False
        self.scope['user'].save()
        # print(f"Disconnecting social socket: {self.scope['user']}")

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        if action == 'friend_list_stp':
            self.send_friend_list()
        elif action == 'request_list_stp':
            self.send_request_list()
        elif action == 'recipient_list_stp':
            self.send_recipient_list()
        print(f"Message Recu: {action}")

    def send_friend_list(self):
        user = self.scope['user']
        friends = FriendList.objects.filter(Q(user1=user) | Q(user2=user))
        my_friend_list = {}
        for friend in friends:
            friend_user = User.objects.filter(username=friend).get()
            my_friend_list['username'] = friend_user.username
            my_friend_list['is_active'] = friend_user.is_connected
            json_data = json.dumps(my_friend_list)
            print(json_data)
            self.send(json_data)

    def send_request_list(self):
        user = self.scope['user']
        requested = FriendRequest.objects.filter(requester=user)
        my_request_list = {}
        print(requested)

    def send_recipient_list(self):
        pass

# message_recu = text_data_json["message"]
# print(f"json user: {serializers.serialize('json', my_friend_list)}")
# text_data = serializers.serialize('json', friends)
# print(f"Friend User: {friend_user.username}")
# print(f"Friend User: {friend_user.is_connected}")
