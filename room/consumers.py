import json

from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    # one instance per open WS; same-room consumers share a group.

    async def connect(self):
        # join the room's group, then accept the handshake.
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # leave the group so dead sockets don't get broadcasts.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # entry point when the browser sends a frame to us.
    async def receive(self, text_data: str) -> None:
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        # persist, then fan out to everyone in the room.
        await self.save_message(username, room, message)

        # 'type' tells channels which method to call on each receiver.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # called on every consumer in the group, sender included.
    async def chat_message(self, event_data: dict[str, str]) -> None:
        message = event_data['message']
        username = event_data['username']

        # ship the frame down this socket.
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # sync_to_async because ORM is sync and we're in an async coroutine.
    @sync_to_async
    def save_message(self, username: str, room: str, message: str) -> None:
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        Message.objects.create(user=user, room=room, content=message)
