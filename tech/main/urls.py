from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),  # Главная страница
    path('accounts/profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('menu/', views.menu, name='menu'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/delete/<int:ingredient_id>/', views.delete_ingredient, name='delete_ingredient'),
    path('inventory/edit/<int:ingredient_id>/', views.edit_ingredient, name='edit_ingredient'),
    path('purchase/', views.purchase, name='purchase'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('menu_form/', views.menu_form, name='menu_form'),
    path('menu/<int:menu_item_id>/delete/', views.confirm_delete_menu_item, name='confirm_delete_menu_item'),
    path('view_requirements/<int:menu_item_id>/', views.view_requirements, name='view_requirements'),
]
