from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Account, Notification


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'about_me',
            'phone',
            'photo',
            'password1',
            'password2',
        ]


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = Account
        fields = [
            'email',
            'password1',
        ]


class NotificationSettingForm(ModelForm):
    class Meta:
        model = Notification
        fields = [
            'mail',
            'telegram',
        ]
