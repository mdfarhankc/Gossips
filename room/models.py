from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.text import slugify

MAX_MESSAGE_LEN = 2000


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_rooms',
    )
    is_private = models.BooleanField(default=False, db_index=True)
    invited_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='invited_rooms',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        # collision-resilient. unique constraint at the DB level is the final guard.
        base = slugify(self.name) or 'room'
        slug = base
        i = 2
        while Room.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='messages',
    )
    content = models.TextField(validators=[MaxLengthValidator(MAX_MESSAGE_LEN)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            # speeds up "load messages of room X in chronological order".
            models.Index(fields=['room', 'created_at']),
        ]

    def __str__(self):
        sender = self.user.username if self.user else '[deleted]'
        return f"{sender}: {self.content[:40]}"
