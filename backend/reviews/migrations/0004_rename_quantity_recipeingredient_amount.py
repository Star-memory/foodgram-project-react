# Generated by Django 3.2 on 2023-07-29 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230726_1408'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='quantity',
            new_name='amount',
        ),
    ]