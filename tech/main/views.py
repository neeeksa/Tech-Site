from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomAuthenticationForm, CustomUserCreationForm


def index(request):
    return render(request, 'main/index.html')


def menu(request):
    return render(request, 'main/menu.html')


def inventory(request):
    return render(request, 'main/inventory.html')


def buy(request):
    return render(request, 'main/buy.html')


def purchase_history(request):
    return render(request, 'main/purchase_history.html')


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
    return render(request, 'main/profile.html')


def profile(request):
    user_nickname = None
    if request.user.is_authenticated:
        user_nickname = request.user.username

    return render(request, 'main/profile.html', {'user_nickname': user_nickname})
