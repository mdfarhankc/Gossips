import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q

from .models import MAX_MESSAGE_LEN, Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    # one instance per open WS; same-room consumers share a group.

    async def connect(self):
        # identity & room derived from the trusted scope, never the client.
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        if not self.user.is_authenticated:
            await self.close(code=4401)
            return

        if not await self._can_access(self.room_name, self.user.id):
            # don't leak whether the room exists or just refuses us — both → 4403.
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        # safe even if connect() rejected — group_discard is a no-op for unjoined groups.
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # entry point when the browser sends a frame to us.
    async def receive(self, text_data: str) -> None:
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message = (data.get('message') or '').strip()
        if not message:
            return
        if len(message) > MAX_MESSAGE_LEN:
            message = message[:MAX_MESSAGE_LEN]

        # re-check on every send so revoked invitees can't keep posting.
        if not await self._can_access(self.room_name, self.user.id):
            await self.close(code=4403)
            return

        username = self.user.username
        await self._save_message(self.user.id, self.room_name, message)

        # 'type' tells channels which method to call on each receiver.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # called on every consumer in the group, sender included.
    async def chat_message(self, event_data: dict[str, str]) -> None:
        await self.send(text_data=json.dumps({
            'message': event_data['message'],
            'username': event_data['username'],
        }))

    @database_sync_to_async
    def _can_access(self, slug: str, user_id: int) -> bool:
        # one query: room must exist AND (be public OR user is owner OR user is invited).
        return Room.objects.filter(slug=slug).filter(
            Q(is_private=False) | Q(owner_id=user_id) | Q(invited_users__id=user_id)
        ).exists()

    @database_sync_to_async
    def _save_message(self, user_id: int, room_slug: str, message: str) -> None:
        Message.objects.create(
            user_id=user_id,
            room=Room.objects.get(slug=room_slug),
            content=message,
        )
