from django import forms
from django.contrib.auth import get_user_model

from .models import Room


class RoomForm(forms.ModelForm):
    invited_users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.filter(is_superuser=False),
        required=False,
    )

    class Meta:
        model = Room
        fields = ['name', 'slug', 'description', 'is_private']

    def clean(self):
        cleaned_data = super().clean()
        is_private = cleaned_data.get('is_private')
        invited_users = cleaned_data.get('invited_users')

        if is_private and not invited_users:
            raise forms.ValidationError('Private rooms must have invited users.')
