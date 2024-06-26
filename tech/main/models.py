from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Добавляем поле price
    available_quantity = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)  # Добавляем новое поле quantity
    ingredients = models.ManyToManyField(Ingredient, through='RecipeRequirement')

    def __str__(self):
        return self.name


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='recipe_requirements')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField()


class Purchase(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default=1, related_name='purchases')
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.purchase_date}'


class PurchasedIngredient(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient.name} - {self.quantity}'


class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)  # Новое поле для элементов меню
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        if self.ingredient:
            return f'{self.user.username} - {self.ingredient.name} - {self.quantity} - {self.total_price} - {self.purchase_date}'
        elif self.menu_item:
            return f'{self.user.username} - {self.menu_item.name} - {self.quantity} - {self.total_price} - {self.purchase_date}'
        else:
            return f'{self.user.username} - No item - {self.quantity} - {self.total_price} - {self.purchase_date}'
