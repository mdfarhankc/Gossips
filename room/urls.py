from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateRoom.as_view(), name='create_room'),
    path('mine/', views.UserCreatedRoomsView.as_view(), name='my_rooms'),
    path('invited/', views.InvitedRoomsView.as_view(), name='invited_rooms'),
    path('<slug:slug>/invite/', views.ManageInvitees.as_view(), name='manage_invitees'),
    path('<slug:slug>/delete/', views.DeleteRoom.as_view(), name='delete_room'),
    path('<slug:slug>/', views.room_detail, name='room_detail'),
    path('', views.rooms, name='rooms'),
]
