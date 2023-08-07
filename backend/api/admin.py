from django.contrib import admin
from reviews.models import (FavoriteRecipe, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCartRecipe, Tag)
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'is_superuser')
    list_filter = ('username', 'email')


class RecipeIngredientAdmin(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientAdmin, )
    list_display = ('id', 'author', 'name', 'image',
                    'text', 'pub_date', 'get_total_favorites')
    list_filter = ('name', 'author', 'tags')

    def get_total_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()

    get_total_favorites.short_description = 'Total Favorites'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingCartRecipe)
admin.site.register(RecipeIngredient)
