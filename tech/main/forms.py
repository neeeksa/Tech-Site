from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Ingredient, Purchase, MenuItem, RecipeRequirement, PurchaseHistory
from django.forms import inlineformset_factory



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


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'quantity']  # Добавляем поле quantity


class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ['ingredient', 'quantity']


class PurchaseMenuItemForm(forms.ModelForm):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.all(), label='Menu item')
    quantity = forms.IntegerField(min_value=1, label='Quantity')

    class Meta:
        model = PurchaseHistory
        fields = ['menu_item', 'quantity']


class EditMenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'quantity']