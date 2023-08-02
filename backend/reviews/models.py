from django.db import models

from colorfield.fields import ColorField

from django.core.exceptions import ValidationError

from constants import constants

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=constants.TAG_NAME_MAX_LENGHT,
                            verbose_name='название тэга')
    color = ColorField(verbose_name='цвет тэга')
    slug = models.SlugField(
        unique=True,
        max_length=constants.TAG_SLUG_MAX_LENGHT,
        verbose_name='slug тэга'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return str(self.id)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=constants.INGREDIENT_NAME_MAX_LENGHT,
        verbose_name='название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=constants.INGREDIENT_MEASUREMENT_MAX_LENGHT,
        verbose_name='единица измерения'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='автор рецепта')
    name = models.CharField(
        max_length=constants.RECIPE_NAME_MAX_LENGHT,
        verbose_name='название рецепта'
    )
    image = models.ImageField(
        upload_to='recipe_images/', verbose_name='изображение рецепта')
    text = models.TextField(verbose_name='описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ингредиенты'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='дата публикации'
    )
    tags = models.ManyToManyField(Tag, verbose_name='тэги')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовления')

    class Meta:
        ordering = ['id']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def validator(self):
        if self.cooking_time <= 1:
            raise ValidationError(
                {'cooking_time': 'Значение должно быть хотя бы 1 минута.'})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='связанный рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        verbose_name='связанные ингредиенты')
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество ингредиента')

    class Meta:
        verbose_name = 'ингредиент для рецепта'
        verbose_name_plural = 'ингредиент для рецептов'

    def validator(self):
        if self.amount <= 1:
            raise ValidationError(
                {'amount':
                 'Минимальное количество ингредиента должно быть хотя бы 1.'})


class BaseRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт')

    class Meta:
        abstract = True
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uniq_recipe'
            )
        ]


class FavoriteRecipe(BaseRecipe):

    class Meta:
        verbose_name = 'рецепт для подписки'
        verbose_name_plural = 'рецепты для подписки'


class ShoppingCartRecipe(BaseRecipe):

    class Meta:
        verbose_name = 'рецепт для карточки'
        verbose_name_plural = 'рецепты для карточки'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower', verbose_name='подписчик')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following', verbose_name='автор')

    class Meta:
        ordering = ['id']
        verbose_name = 'подписка на автора'
        verbose_name_plural = 'подписки на автора'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='uniq_follow')
        ]
