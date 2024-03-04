from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Ingredient, Purchase


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']  # Добавьте сюда поля, которые вы хотите видеть в форме регистрации


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User


class PurchaseForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, label='Quantity')

    class Meta:
        model = Purchase
        fields = ['ingredient', 'quantity']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit_price']
