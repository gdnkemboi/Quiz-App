from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import UserProfile

class UserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )

class UserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=32)
    class Meta():
        model = UserProfile
        fields = ["profile_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial value for the 'username' field
        user = kwargs.get('instance', None)
        if user:
            self.fields['username'].initial = user.user.username