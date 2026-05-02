from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = ['username', 'email']  # required by autocomplete_fields elsewhere
