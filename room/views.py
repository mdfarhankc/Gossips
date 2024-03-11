from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .models import Room, Message
from .forms import RoomForm

@login_required
def Rooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        data = {'rooms': rooms}
        return render(request, 'room/rooms.html', data)


@login_required
def RoomDetail(request, slug):
    if request.method == 'GET':
        room = Room.objects.get(slug=slug)
        messages = Message.objects.filter(room=room)
        data = {'room': room, 'messages': messages, 'messagesLen': len(messages)}
        return render(request, 'room/room_detail.html', data)


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
            return redirect('rooms')
        return render(request, self.template_name, data)
    

@method_decorator(login_required, name='dispatch')
class UserCreatedRoomsView(ListView):
    model = Room
    template_name = 'room/my_rooms.html'
    context_object_name = 'created_rooms'

    def get_queryset(self):
        return Room.objects.filter(owner=self.request.user)