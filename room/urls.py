from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateRoom.as_view(), name='create_room'),
    path('<slug:slug>/', views.RoomDetail, name='room_detail'),
    path('', views.Rooms, name='rooms'),
]