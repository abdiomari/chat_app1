# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, Message

online_users = {}


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name       = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user            = self.scope['user']
        self.username        = self.user.username if self.user.is_authenticated else 'Anonymous'

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        if self.room_group_name not in online_users:
            online_users[self.room_group_name] = {}
        online_users[self.room_group_name][self.channel_name] = self.username

        self.accept()
        self.broadcast_user_list()

    def disconnect(self, close_code):
        if self.room_group_name in online_users:
            online_users[self.room_group_name].pop(self.channel_name, None)
            if not online_users[self.room_group_name]:
                del online_users[self.room_group_name]

        self.broadcast_user_list()

        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        data     = json.loads(text_data)
        message  = data['message']
        username = self.username

        room, _ = Room.objects.get_or_create(name=self.room_name)
        msg_obj = Message.objects.create(
            room    = room,
            user    = self.user if self.user.is_authenticated else None,
            content = message
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type'      : 'chat_message',
                'message'   : message,
                'username'  : username,
                'message_id': msg_obj.id,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type'      : 'message',
            'message'   : event['message'],
            'username'  : event['username'],
            'message_id': event['message_id'],
        }))

    def user_list(self, event):
        self.send(text_data=json.dumps({
            'type' : 'user_list',
            'users': event['users'],
        }))

    def broadcast_user_list(self):
        users = list(online_users.get(self.room_group_name, {}).values())
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'user_list', 'users': users}
        )