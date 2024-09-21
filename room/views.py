from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView

from .models import Room, Message
from .forms import RoomForm

@login_required
def Rooms(request):
    rooms = Room.objects.filter(is_private=False).order_by('-date_added')
    data = {'rooms': rooms}
    return render(request, 'room/rooms.html', data)

@login_required
def RoomDetail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room)
    data = {'room': room, 'messages': messages, 'messagesLen': len(messages)}
    return render(request, 'room/room_detail.html', data)


@login_required
def PrivateRoomDetail(request, slug):
    room = get_object_or_404(Room, slug=slug)

    if room.is_private:
        if request.user == room.owner or request.user in room.invited_users.all():
            messages = Message.objects.filter(room=room)
            data = {'room': room, 'messages': messages, 'messagesLen': len(messages)}
            return render(request, 'room/room_detail.html', data)
    else:
        return HttpResponseForbidden("You are not authorized to enter this room.")
    
    

@method_decorator(login_required, name='dispatch')
class InvitedRoomsView(View):
    template_name = 'room/invited_rooms.html'

    def get(self, request):
        invited_rooms = Room.objects.filter(invited_users=request.user)
        data = {'invited_rooms': invited_rooms}
        return render(request, self.template_name, data)


@method_decorator(login_required, name='dispatch')
class CreateRoom(View):
    template_name = 'room/create_room.html'
    
    def get(self, request):
        form = RoomForm()
        data = {'form': form}
        return render(request, 'room/create_room.html', data)
    
    def post(self, request):
        form = RoomForm(request.POST)
        data = {'form': form}
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            form.save_m2m()
            return redirect('my_rooms')
        return render(request, self.template_name, data)
    

@method_decorator(login_required, name='dispatch')
class UserCreatedRoomsView(ListView):
    model = Room
    template_name = 'room/my_rooms.html'
    context_object_name = 'created_rooms'

    def get_queryset(self):
        return Room.objects.filter(owner=self.request.user)