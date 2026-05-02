from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateRoom.as_view(), name='create_room'),
    path('my_rooms/', views.UserCreatedRoomsView.as_view(), name='my_rooms'),
    path('invited_rooms/', views.InvitedRoomsView.as_view(), name='invited_rooms'),
    path('private/<slug:slug>/', views.private_room_detail, name='private_room_detail'),
    path('<slug:slug>/', views.room_detail, name='room_detail'),
    path('', views.rooms, name='rooms'),
]