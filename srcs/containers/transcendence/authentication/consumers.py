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
        print(f"Message Recu, action: {action}")

    def send_friend_list(self):
        user = self.scope['user']
        friends = FriendList.objects.filter(Q(user1=user) | Q(user2=user))
        my_friend_list = {'action': 'friend_list', 'friend_list': {'friends': {}}}
        # my_friend_list = {}
        # my_friend_list['friend_list'] = {}
        # my_friend_list['friend_list']['friends'] = {}
        for friend in friends:
            friend_user = friend.user1 if friend.user1 != user else friend.user2
            my_friend_list['friend_list']['friends'][friend_user.username] = {'is_connected': friend_user.is_connected}
        
        json_data = json.dumps(my_friend_list)
        self.send(text_data=json_data)

# list_social['requested_list'] = self.request_list()
# list_social['received_list'] = self.recipient_list()

    # def friend_list(self):
    #     user = self.scope['user']
    #     friends = FriendList.objects.filter(Q(user1=user) | Q(user2=user))
    #     my_friend_list = {}
    #     for friend in friends:
    #         if (friend.user1 != user):
    #             friend_user = User.objects.filter(username=friend.user1.username).get()
    #         else:
    #             friend_user = User.objects.filter(username=friend.user2.username).get()
    #         my_friend_list[friend_user.username] = {'is_connected': friend_user.is_connected}
    #     print(f"friends: {my_friend_list}")
    #     return my_friend_list

    def request_list(self):
        user = self.scope['user']
        requested = FriendRequest.objects.filter(requester=user)
        my_request_list = {}
        for request in requested:
            requested_user = User.objects.filter(username=request.recipient.username).get()
            my_request_list[requested_user.username] = {'is_connected': requested_user.is_connected}
        return my_request_list

    def recipient_list(self):
        user = self.scope['user']
        recipient = FriendRequest.objects.filter(recipient=user)
        my_recipient_list = {}
        for receiver in recipient:
            recipient_user = User.objects.filter(username=receiver.requester.username).get()
            my_recipient_list[recipient_user.username] = {'is_connected': recipient_user.is_connected}
        return my_recipient_list

    def create_request(self, username):
        requester = self.scope['user']
        recipient = User.objects.filter(username=username)
        if recipient.exists():
            FriendRequest.objects.create(requester=requester, recipient=recipient.get())
            print(f"Friend request create between {requester} and {recipient}")
            # Send info back to the user
        else:
            print("User not found !")
            # Send info back to the user


# message_recu = text_data_json["message"]
# print(f"json user: {serializers.serialize('json', my_friend_list)}")
# text_data = serializers.serialize('json', friends)
# print(f"Friend User: {friend_user.username}")
# print(f"Friend User: {friend_user.is_connected}")
