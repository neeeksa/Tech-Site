from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework import routers
from .views import IngredientsApi, MenuItemApi

router = routers.DefaultRouter()
router.register(r'api/ingredient', IngredientsApi)
router.register(r'api/menu_item', MenuItemApi)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),  # Главная страница
    path('accounts/profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('menu/', views.menu, name='menu'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/edit/<int:ingredient_id>/', views.edit_ingredient, name='edit_ingredient'),
    path('purchase/', views.purchase, name='purchase'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('menu/<int:menu_item_id>/delete/', views.confirm_delete_menu_item, name='confirm_delete_menu_item'),
    path('inventory/<int:ingredient_id>/delete/', views.confirm_delete_ingredient_item,
         name='confirm_delete_ingredient_item'),
    path('purchase_menu/', views.purchase_menu, name='purchase_menu'),
    path('menu/<int:pk>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('', include(router.urls))
]
