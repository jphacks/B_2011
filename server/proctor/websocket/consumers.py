from channels.generic.websocket import WebsocketConsumer
from sent_messages.serizlizers import MessageSerializer
import json


class ExamineeConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.send(text_data=json.dumps({
            'message': 'received message'
        }))
