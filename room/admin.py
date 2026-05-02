from django.contrib import admin

from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'owner', 'is_private', 'created_at']
    list_filter = ['is_private', 'created_at']
    search_fields = ['name', 'slug']
    autocomplete_fields = ['owner']
    filter_horizontal = ['invited_users']
    readonly_fields = ['created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'short_content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
    autocomplete_fields = ['room', 'user']
    readonly_fields = ['created_at']

    @admin.display(description='content')
    def short_content(self, obj):
        return (obj.content[:60] + '…') if len(obj.content) > 60 else obj.content