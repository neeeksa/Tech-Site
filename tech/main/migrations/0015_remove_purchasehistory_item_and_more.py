# Generated by Django 5.0.3 on 2024-03-05 11:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_item_remove_purchasehistory_ingredient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasehistory',
            name='item',
        ),
        migrations.RemoveField(
            model_name='purchasemenuitem',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='purchasemenuitem',
            name='user',
        ),
        migrations.AddField(
            model_name='purchasehistory',
            name='ingredient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ingredient'),
        ),
        migrations.AddField(
            model_name='purchasehistory',
            name='menu_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.menuitem'),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='PurchaseMenuItem',
        ),
    ]