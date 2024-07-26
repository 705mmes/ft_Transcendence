import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print(self.scope['user'])

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = "Caca"
        await self.send(text_data=json.dumps({
            'message': f'You said: {message}'
        }))
