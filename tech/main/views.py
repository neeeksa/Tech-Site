from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import (CustomAuthenticationForm, CustomUserCreationForm, PurchaseForm, IngredientForm, MenuItemForm,
                    PurchaseMenuItemForm, EditMenuItemForm)

from .models import Ingredient, PurchaseHistory, MenuItem
from django.utils import timezone

from .serializers import IngredientSerializer, MenuItemSerializer
from rest_framework import viewsets


# ----------------------- api -----------------------
class IngredientsApi(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']


class MenuItemApi(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    http_method_names = ['get']


def edit_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = EditMenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Перенаправляем на главную страницу после редактирования
    else:
        form = EditMenuItemForm(instance=menu_item)
    return render(request, 'main/edit_menu_item.html', {'form': form, 'menu_item': menu_item})


def purchase_menu(request):
    if request.method == 'POST':
        form = PurchaseMenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.cleaned_data['menu_item']
            quantity = form.cleaned_data['quantity']

            # Проверяем, что количество элемента меню больше нуля
            if menu_item.quantity < quantity:
                form.add_error(None, "Not enough stock for this item.")
                return render(request, 'main/purchase_menu.html', {'form': form})

            purchase_instance = form.save(commit=False)
            purchase_instance.user = request.user
            purchase_instance.total_price = menu_item.price * quantity
            purchase_instance.purchase_date = timezone.now()
            purchase_instance.save()

            # Обновляем количество доступных элементов меню
            menu_item.quantity -= quantity
            menu_item.save()

            return redirect('index')  # Перенаправляем на главную страницу после покупки
    else:
        form = PurchaseMenuItemForm()

    return render(request, 'main/purchase_menu.html', {'form': form})


def index(request):
    return render(request, 'main/index.html')


def menu(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuItemForm()

    menu_items = MenuItem.objects.all()
    ingredients = Ingredient.objects.all()  # Получаем все ингредиенты
    context = {
        'menu_items': menu_items,
        'form': form,
        'ingredients': ingredients,  # Передаем список ингредиентов в контекст
    }
    return render(request, 'main/menu.html', context)


def confirm_delete_menu_item(request, menu_item_id):
    menu_item = MenuItem.objects.get(pk=menu_item_id)
    if request.method == 'POST':
        menu_item.delete()
        return redirect('menu')  # Перенаправляем на страницу меню после удаления
    return render(request, 'main/confirm_delete_menu_item.html', {'menu_item': menu_item})


def inventory(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            quantity = form.cleaned_data['quantity']
            unit_price = form.cleaned_data['unit_price']

            # Пытаемся найти ингредиент с таким же именем
            ingredient, created = Ingredient.objects.get_or_create(name=name, defaults={'quantity': quantity,
                                                                                        'unit_price': unit_price})

            if not created:
                # Если ингредиент с таким именем уже существует, обновляем его количество и цену
                ingredient.quantity += quantity
                ingredient.unit_price = unit_price
                ingredient.save()

            # Перенаправляем пользователя на страницу инвентаря после добавления/обновления ингредиента
            return redirect('inventory')
    else:
        form = IngredientForm()

    ingredients = Ingredient.objects.all()
    context = {
        'ingredients': ingredients,
        'form': form,
    }
    return render(request, 'main/inventory.html', context)


def confirm_delete_ingredient_item(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('inventory')  # Перенаправляем на страницу инвентаря после удаления
    return render(request, 'main/confirm_delete_ingredient_item.html', {'ingredient': ingredient})


def edit_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = IngredientForm(instance=ingredient)

    return render(request, 'main/edit_ingredient.html', {'form': form})


def purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase_instance = form.save(commit=False)
            purchase_instance.user = request.user
            purchase_instance.total_price = purchase_instance.ingredient.unit_price * purchase_instance.quantity
            purchase_instance.purchase_date = timezone.now()

            if purchase_instance.ingredient.quantity < purchase_instance.quantity:
                # Если запрашиваемое количество товара больше, чем есть в наличии, возвращаемся к странице покупки с сообщением об ошибке
                form.add_error('quantity', "Not enough stock available for this ingredient.")
                return render(request, 'main/purchase.html', {'form': form})

            purchase_instance.save()
            purchase_instance.ingredient.quantity -= purchase_instance.quantity
            purchase_instance.ingredient.save()

            PurchaseHistory.objects.create(
                user=request.user,
                ingredient=purchase_instance.ingredient,
                quantity=purchase_instance.quantity,
                total_price=purchase_instance.total_price,
                purchase_date=purchase_instance.purchase_date
            )

            return redirect('index')
    else:
        form = PurchaseForm()

    context = {
        'form': form,
    }
    return render(request, 'main/purchase.html', context)


def purchase_history(request):
    purchase_history = PurchaseHistory.objects.filter(user=request.user)
    return render(request, 'main/purchase_history.html', {'purchase_history': purchase_history})


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'register:login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})


def profile(request):
    user_nickname = None
    if request.user.is_authenticated:
        user_nickname = request.user.username

    return render(request, 'main/profile.html', {'user_nickname': user_nickname})
