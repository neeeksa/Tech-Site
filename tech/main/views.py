from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import (CustomAuthenticationForm, CustomUserCreationForm, PurchaseForm, IngredientForm, MenuItemForm,
                    RecipeRequirementForm)
from .models import Ingredient, PurchaseHistory, MenuItem, RecipeRequirement
from django.utils import timezone


def index(request):
    return render(request, 'main/index.html')


def view_requirements(request, menu_item_id):
    menu_item = MenuItem.objects.get(pk=menu_item_id)
    requirements = RecipeRequirement.objects.filter(menu_item=menu_item)
    return render(request, 'main/view_requirements.html', {'menu_item': menu_item, 'requirements': requirements})


def menu_form(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        requirement_form = RecipeRequirementForm(request.POST)
        if form.is_valid():
            menu_item = form.save()  # Сохраняем новый элемент меню
            return redirect('view_requirements', menu_item_id=menu_item.id)  # Перенаправляем на страницу с требованиями к рецепту
        elif requirement_form.is_valid():
            requirement_form.save()  # Сохраняем требование к рецепту
            return redirect('menu')  # Перенаправляем на страницу меню после сохранения
    else:
        form = MenuItemForm()
        requirement_form = RecipeRequirementForm()

    context = {
        'form': form,
        'requirement_form': requirement_form,
        'menu_item_id': request.GET.get('menu_item_id')
    }
    return render(request, 'main/menu_form.html', context)


def menu(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuItemForm()

    menu_items = MenuItem.objects.all()
    context = {
        'menu_items': menu_items,
        'form': form,
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
            price = form.cleaned_data['unit_price']

            # Пытаемся найти ингредиент с таким же именем
            ingredient, created = Ingredient.objects.get_or_create(name=name, defaults={'quantity': quantity, 'price': price})

            if not created:
                # Если ингредиент с таким именем уже существует, обновляем его количество и цену
                ingredient.quantity += quantity
                ingredient.price = price
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


def delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    ingredient.delete()
    return redirect('inventory')


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
            purchase_instance.total_price = purchase_instance.ingredient.price * purchase_instance.quantity

            # Используем timezone.now() для создания "aware datetime"
            purchase_instance.purchase_date = timezone.now()

            purchase_instance.save()

            # Создаем запись в истории покупок
            purchase_history_entry = PurchaseHistory.objects.create(
                user=request.user,
                ingredient=purchase_instance.ingredient,
                quantity=purchase_instance.quantity,
                total_price=purchase_instance.total_price,
                purchase_date=purchase_instance.purchase_date  # Передаем "aware datetime"
            )
            purchase_history_entry.save()

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
