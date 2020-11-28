from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth import get_user_model
User = get_user_model()
from channels.db import database_sync_to_async
from .serializers import ChatPostSerializer



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        # a = User.objects.get_or_create(user = self.scope['user'])
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room_id':self.room_name
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']
     
	
        self.send(text_data=json.dumps({
            'message': message,
            'username':username
        }))

    #@database_sync_to_async
    def _create_chat(self, content):
        serializer = ChatPostSerializer(data=content)
        serializer.is_valid(raise_exception=True)
        room = serializer.create(serializer.validated_data)
        return room