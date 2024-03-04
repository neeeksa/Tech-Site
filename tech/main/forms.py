from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']  # Добавьте сюда поля, которые вы хотите видеть в форме регистрации


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
