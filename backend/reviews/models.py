from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(
        unique=True,
        max_length=200
    )

    class Meta:
        ordering = ['id']


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='recipe_images/')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField()

    class Meta:
        ordering = ['id']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class ShoppingCartRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='uniq_cart')
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='uniq_favoerite')
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='uniq_follow')
        ]
