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
        if action == 'social_list':
            self.send_social()
        print(f"Message Recu: {action}")

    def send_social(self):
        user = self.scope['user']
        friends = FriendList.objects.filter(Q(user1=user) | Q(user2=user))
        list_social = {}
        list_social['social_list'] = {}
        list_social['social_list']['friends'] = self.friend_list()
        list_social['social_list']['requested'] = self.request_list()
        list_social['social_list']['received'] = self.recipient_list()
        json_data = json.dumps(list_social)
        print(json_data)
        self.send(json_data)



    def friend_list(self):
        user = self.scope['user']
        friends = FriendList.objects.filter(Q(user1=user) | Q(user2=user))
        my_friend_list = {}
        for friend in friends:
            friend_user = User.objects.filter(username=friend).get()
            my_friend_list[friend_user.username] = {'is_connected': friend_user.is_connected}
        print(f"friends: {my_friend_list}")
        return my_friend_list

    def request_list(self):
        user = self.scope['user']
        requested = FriendRequest.objects.filter(requester=user)
        my_request_list = {}
        for request in requested:
            requested_user = User.objects.filter(username=request.recipient.username).get()
            my_request_list[requested_user.username] = {'is_connected': requested_user.is_connected}
        print(f"Request: {my_request_list}")
        return my_request_list

    def recipient_list(self):
        user = self.scope['user']
        recipient = FriendRequest.objects.filter(recipient=user)
        my_recipient_list = {}
        for receiver in recipient:
            recipient_user = User.objects.filter(username=receiver.requester.username).get()
            my_recipient_list[recipient_user.username] = {'is_connected': recipient_user.is_connected}
        print(f"Receive: {my_recipient_list}")
        return my_recipient_list

# message_recu = text_data_json["message"]
# print(f"json user: {serializers.serialize('json', my_friend_list)}")
# text_data = serializers.serialize('json', friends)
# print(f"Friend User: {friend_user.username}")
# print(f"Friend User: {friend_user.is_connected}")
