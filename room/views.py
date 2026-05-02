from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView

from .models import Room, Message
from .forms import RoomForm


@login_required
def rooms(request):
    public_rooms = Room.objects.filter(is_private=False)
    return render(request, 'room/rooms.html', {'rooms': public_rooms})


@login_required
def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)

    if room.is_private and request.user != room.owner and request.user not in room.invited_users.all():
        return HttpResponseForbidden("You are not authorized to enter this room.")

    messages = Message.objects.filter(room=room)
    data = {'room': room, 'messages': messages, 'messagesLen': len(messages)}
    return render(request, 'room/room_detail.html', data)


@method_decorator(login_required, name='dispatch')
class InvitedRoomsView(View):
    template_name = 'room/invited_rooms.html'

    def get(self, request):
        invited_rooms = Room.objects.filter(invited_users=request.user)
        return render(request, self.template_name, {'invited_rooms': invited_rooms})


@method_decorator(login_required, name='dispatch')
class CreateRoom(View):
    template_name = 'room/create_room.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RoomForm()})

    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            form.save_m2m()
            return redirect('my_rooms')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class UserCreatedRoomsView(ListView):
    model = Room
    template_name = 'room/my_rooms.html'
    context_object_name = 'created_rooms'

    def get_queryset(self):
        return Room.objects.filter(owner=self.request.user)
