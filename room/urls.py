from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateRoom.as_view(), name='create_room'),
    path('my_rooms/', views.UserCreatedRoomsView.as_view(), name='my_rooms'),
    path('<slug:slug>/', views.RoomDetail, name='room_detail'),
    path('', views.Rooms, name='rooms'),
]