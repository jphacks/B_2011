from channels.generic.websocket import AsyncWebsocketConsumer
from sent_messages.serizlizers import MessageSerializer
from channels.db import database_sync_to_async

import json

class ExamineeConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['exam_id']
        self.room_group_name = 'chat_{}'.format(self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket`
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json

        #send message to users from examinees
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'examinee_message',
                'message': message
            }
        )

        #save message to database
        await self.save_message(text_data)

    # Receive message from users
    async def user_message(self, event):
        message = event['message']

        # Send message to WebSocket
        print(message)
        await self.send(text_data=message)

    async def examinee_message(self, event):
        pass

    @database_sync_to_async
    def save_message(self, text):
        message = json.loads(text)
        serializer = MessageSerializer(data=message)
        serializer.is_valid(raise_exception=True)
        serializer.save()

class UserConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['exam_id']
        self.room_group_name = 'chat_{}'.format(self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket`
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #send message to users from examinees

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_message',
                'message': message
            }
        )

    # Receive message from examinees
    async def examinee_message(self, event):
        message = event['message']
        if message['alert']==0:
            return 0
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    async def user_message(self, event):
        pass
