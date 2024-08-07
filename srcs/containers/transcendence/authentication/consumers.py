import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, FriendList, FriendRequest
from django.db.models import Q
from django.core import serializers


class ActiveConsumer(WebsocketConsumer):
    def connect(self):
        print(f"Connecting to : {self.scope['user']}")
        self.scope['user'].is_connected = True
        self.scope['user'].save()
        self.room_name = "social_" + self.scope['user'].username
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.scope['user'].is_connected = False
        self.scope['user'].save()
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive(self, text_data):
        print("Message recu sur ws social !")
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        if action == 'friend_list':
            self.send_friend_list()
        elif action == 'request_list':
            self.send_request_list()
        elif action == 'pending_list':
            self.send_pending_list()
        elif action == 'friend_request':
            self.create_request(text_data_json['username'])
        elif action == 'remove_friend':
            self.remove_friend(text_data_json['target'])
        elif action == 'accept_friend_request':
            self.accept_request(text_data_json['target'])
        elif action == 'deny_friend_request':
            self.deny_request(text_data_json['target'])
        print(f"Message Recu, action: {action}")
        print(text_data_json)

    def send_friend_list(self):
        user = self.scope['user']
        friends = FriendList.objects.filter(Q(user1=user) | Q(user2=user))
        my_friend_list = {'action': 'friend_list', 'friend_list': {'friends': {}}}
        for friend in friends:
            friend_user = friend.user1 if friend.user1 != user else friend.user2
            my_friend_list['friend_list']['friends'][friend_user.username] = {'is_connected': friend_user.is_connected}
        json_data = json.dumps(my_friend_list)
        self.send(json_data)

    def send_request_list(self):
        user = self.scope['user']
        recipient = FriendRequest.objects.filter(recipient=user)
        my_recipient_list = {'action': 'request_list', 'request_list': {'request': {}}}
        for receiver in recipient:
            recipient_user = User.objects.filter(username=receiver.requester.username).get()
            my_recipient_list['request_list']['request'][recipient_user.username] = {
                'is_connected': recipient_user.is_connected}
        print(my_recipient_list)
        json_data = json.dumps(my_recipient_list)
        self.send(json_data)

    def send_pending_list(self):
        user = self.scope['user']
        requested = FriendRequest.objects.filter(requester=user)
        my_request_list = {'action': 'pending_list', 'pending_list': {'pending': {}}}
        for request in requested:
            requested_user = User.objects.filter(username=request.recipient.username).get()
            my_request_list['pending_list']['pending'][requested_user.username] = {
                'is_connected': requested_user.is_connected}
        print(my_request_list)
        json_data = json.dumps(my_request_list)
        self.send(json_data)

    def create_request(self, username):
        requester = self.scope['user']
        recipient = User.objects.filter(username=username)
        if recipient.exists():
            if not FriendRequest.objects.filter(requester=requester, recipient=recipient.get()).exists():
                FriendRequest.objects.create(requester=requester, recipient=recipient.get())
                print(f"Friend request create between {requester} and {recipient}")
            else:
                print(f"Request already exist !")
            # Send info back to the user
        else:
            print("User not found !")
            # Send info back to the user


    def send_info(self, event):
        data = event['data']
        self.send(text_data=json.dumps(data))

    def remove_friend(self, target_name):
        target = User.objects.filter(username=target_name).get()
        me = self.scope['user']
        info = {'action': 'remove_friend', 'target': target_name}
        if FriendList.objects.filter(Q(user1=me) | Q(user2=target)).exists():
            FriendList.objects.filter(Q(user1=me) | Q(user2=target)).delete()
        elif FriendList.objects.filter(Q(user1=target) | Q(user2=me)).exists():
            FriendList.objects.filter(Q(user1=target) | Q(user2=me)).delete()
        print("FriendShip delete !")
        async_to_sync(self.channel_layer.group_add)("social_" + target_name, self.channel_name)
        async_to_sync(self.channel_layer.group_send)("social_" + target_name, { 'type': 'send_info', 'data': info })

    def accept_request(self, target_name):
        target = User.objects.filter(username=target_name).get()
        me = self.scope['user']
        info = {'action': 'accept_friend_request', 'target': target_name, 'is_connected': target.is_connected }
        if not FriendList.objects.filter((Q(user1=me) & Q(user2=target)) | (Q(user1=target) & Q(user2=me))).exists():
            FriendList.objects.create(user1=me, user2=target)
        print("Accept friend request !")
        async_to_sync(self.channel_layer.group_add)("social_" + target_name, self.channel_name)
        async_to_sync(self.channel_layer.group_send)("social_" + target_name, {'type': 'send_info', 'data': info})

    def deny_request(self, target_name):
        target = User.objects.filter(username=target_name).get()
        me = self.scope['user']
        info = {'action': 'deny_friend_request', 'target': target_name}
        if FriendRequest.objects.filter(Q(requester=me) | Q(recipient=target)).exists():
            FriendRequest.objects.filter(Q(requester=me) | Q(recipient=target)).delete()
        elif FriendRequest.objects.filter(Q(requester=target) | Q(recipient=me)).exists():
            FriendRequest.objects.filter(Q(requester=target) | Q(recipient=me)).delete()
        print("Deny friend request !")
        async_to_sync(self.channel_layer.group_add)("social_" + target_name, self.channel_name)
        async_to_sync(self.channel_layer.group_send)("social_" + target_name, {'type': 'send_info', 'data': info})

    def cancel_pending(self):
        pass



