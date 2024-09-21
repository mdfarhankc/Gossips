from django import forms
from django.contrib.auth.models import User

from .models import Room

class RoomForm(forms.ModelForm):
    invited_users = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_superuser=False), required=False)

    class Meta:
        model = Room
        fields = ['name', 'slug', 'is_private']

    def clean(self):
        cleaned_data = super().clean()
        is_private = cleaned_data.get('is_private')
        invited_users = cleaned_data.get('invited_users')

        if is_private and not invited_users:
            raise forms.ValidationError('Private rooms must have invited users.')
