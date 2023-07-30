from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from django_filters import FilterSet, filters

from reviews.models import Recipe, Tag


class PagePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class IngredientNameFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='is_favorited_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)
