from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    invited_users = models.ManyToManyField(User, related_name='invited_rooms', blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('date_added',)