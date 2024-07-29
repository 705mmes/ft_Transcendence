import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        print(f"Connecting to room: {self.room_name} | {self.scope['user']}")

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        print(f"Added {self.channel_name} to room group: {self.room_group_name} | {self.scope['user']}")

        self.accept()
        print(f"Accepted WebSocket connection from {self.channel_name} | {self.scope['user']}")

    def disconnect(self, close_code):
        # Leave room group
        print(f"Disconnecting from room group: {self.room_group_name} | {self.scope['user']}")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print(f"Removed {self.channel_name} from room group: {self.room_group_name} | {self.scope['user']}")

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        print(f"Received message from WebSocket: {message} | {self.scope['user']}")
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_messages", "message": message}
        )
        print(f"Sent message to room group: {self.room_group_name} | {self.scope['user']}")

    # Receive message from room group
    def chat_messages(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
        print(f"Sent chat message to WebSocket: {message} | {self.scope['user']}")