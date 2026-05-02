from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from .forms import RoomForm
from .models import Message, Room

User = get_user_model()


@login_required
def rooms(request):
    public_rooms = Room.objects.filter(is_private=False).select_related('owner')
    return render(request, 'room/rooms.html', {'rooms': public_rooms})


@login_required
def room_detail(request, slug):
    room = get_object_or_404(Room.objects.select_related('owner'), slug=slug)

    if room.is_private and room.owner_id != request.user.id and not room.invited_users.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden("You are not authorized to enter this room.")

    messages = room.messages.select_related('user')
    return render(request, 'room/room_detail.html', {
        'room': room,
        'messages': messages,
        'messagesLen': messages.count(),
    })


class InvitedRoomsView(LoginRequiredMixin, View):
    template_name = 'room/invited_rooms.html'

    def get(self, request):
        invited_rooms = Room.objects.filter(invited_users=request.user).select_related('owner')
        return render(request, self.template_name, {'invited_rooms': invited_rooms})


class CreateRoom(LoginRequiredMixin, View):
    template_name = 'room/create_room.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RoomForm()})

    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            if room.is_private:
                return redirect('manage_invitees', slug=room.slug)
            return redirect('my_rooms')
        return render(request, self.template_name, {'form': form})


class UserCreatedRoomsView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'room/my_rooms.html'
    context_object_name = 'created_rooms'

    def get_queryset(self):
        return Room.objects.filter(owner=self.request.user)


class _OwnerOnlyView(LoginRequiredMixin, View):
    """shared base — fetch a room and refuse anyone but its owner."""

    def _get_room(self, slug, user):
        room = get_object_or_404(Room, slug=slug)
        if room.owner_id != user.id:
            raise PermissionDenied
        return room


class ManageInvitees(_OwnerOnlyView):
    template_name = 'room/manage_invitees.html'

    def _get_private_room(self, slug, user):
        room = self._get_room(slug, user)
        # public rooms have no invitee semantics — bounce to the room itself.
        if not room.is_private:
            return None, redirect('room_detail', slug=room.slug)
        return room, None

    def get(self, request, slug):
        room, redirect_response = self._get_private_room(slug, request.user)
        if redirect_response:
            return redirect_response
        users = (
            User.objects
            .filter(is_superuser=False)
            .exclude(pk=request.user.pk)
            .order_by('username')
        )
        invited_ids = set(room.invited_users.values_list('id', flat=True))
        return render(request, self.template_name, {
            'room': room,
            'users': users,
            'invited_ids': invited_ids,
        })

    def post(self, request, slug):
        room, redirect_response = self._get_private_room(slug, request.user)
        if redirect_response:
            return redirect_response
        ids = request.POST.getlist('invited_users')
        # filter through the same queryset rules so a malicious post can't sneak in superusers / self.
        new_invitees = (
            User.objects
            .filter(pk__in=ids, is_superuser=False)
            .exclude(pk=request.user.pk)
        )
        room.invited_users.set(new_invitees)
        return redirect('room_detail', slug=room.slug)


class DeleteRoom(_OwnerOnlyView):
    template_name = 'room/delete_room.html'

    def get(self, request, slug):
        room = self._get_room(slug, request.user)
        return render(request, self.template_name, {'room': room})

    def post(self, request, slug):
        room = self._get_room(slug, request.user)
        room.delete()
        return redirect('my_rooms')
