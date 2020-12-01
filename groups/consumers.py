from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth import get_user_model
User = get_user_model()
from channels.db import database_sync_to_async
# from .serializers import ChatPostSerializer
import pickle

from .models import Message, Room
from conference.models import Conference



class ChatConsumer(WebsocketConsumer):

    def get_name(self):
        return User.objects.all()[0].name

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
        user = text_data_json['user']
        conference = text_data_json['conference']
        room = text_data_json['room']
        self.save_chat(user,conference,room, message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room':self.room_name,
                'user':user,
                'conference':conference
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event["room"]
        user = event["user"]
        conference = event["conference"]
        
        self.send(text_data=json.dumps({
            'message': message,
            'username':username,
            'room':room,
            'user':user,
            'conference':conference
        }))

    def save_chat(self,user,conference,room, message):
        room_id = Room.objects.get(id=room)
        user_id = User.objects.get(id=user)
        conf_id = Conference.objects.get(id=conference)
        return Message.objects.create(room=room_id,sender=user_id,conference=conf_id, message=message)