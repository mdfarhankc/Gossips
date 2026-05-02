from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateRoom.as_view(), name='create_room'),
    path('mine/', views.UserCreatedRoomsView.as_view(), name='my_rooms'),
    path('invited/', views.InvitedRoomsView.as_view(), name='invited_rooms'),
    path('<slug:slug>/', views.room_detail, name='room_detail'),
    path('', views.rooms, name='rooms'),
]