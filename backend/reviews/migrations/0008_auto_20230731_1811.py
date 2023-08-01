# Generated by Django 3.2 on 2023-07-31 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0007_alter_tag_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoriterecipe',
            options={'ordering': ['id'], 'verbose_name': 'рецепт для подписки', 'verbose_name_plural': 'рецепты для подписки'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['id'], 'verbose_name': 'подписка на автора', 'verbose_name_plural': 'подписки на автора'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'ингредиент для рецепта', 'verbose_name_plural': 'ингредиент для рецептов'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcartrecipe',
            options={'ordering': ['id'], 'verbose_name': 'рецепт для карточки', 'verbose_name_plural': 'рецепты для карточки'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipe_images/', verbose_name='изображение рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='описание рецепта'),
        ),
    ]