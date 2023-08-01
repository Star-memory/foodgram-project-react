from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Sum

from django.http import HttpResponse

from djoser.views import UserViewSet as DjoserUserViewSet

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User
from reviews.models import (Tag, Recipe, Ingredient, RecipeIngredient,
                            FavoriteRecipe, Follow, ShoppingCartRecipe)


from .utils import (IngredientNameFilter, PagePagination, RecipeFilter)
from .mixins import ListRetriveSet, CreateDestroyMixin
from .permissions import ReadOnlyTag
from .serializers import (TagSerializer, RecipeReadSerializer,
                          RecipeCreateSerializer, FollowSerializer,
                          IngredientSerializer, UserSerializer,
                          PasswordSerializer, UserRegistrationSerializer,
                          FavoriteSerializer, ShoppingCartSerializer)


class UserViewSet(DjoserUserViewSet, CreateDestroyMixin):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated]
            )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if author == user:
                return Response(
                    {'error': 'Вы не можете подписаться на себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return self.create_сustom(
                request, Follow, FollowSerializer,
                obj_field='user', obj_id_field='author',
                obj=user, obj_id=author,
                error_message='Вы уже подписаны на этого пользователя.')
        if request.method == 'DELETE':
            return self.destroy_сustom(
                request, Follow, obj_field='user', obj_id_field='author',
                obj=user, obj_id=author, detail_message='Успешная отписка.')

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated],
            pagination_class=PagePagination)
    def subscriptions(self, request):
        user = request.user
        follow = Follow.objects.filter(user=user)
        paginator = self.pagination_class()
        recipes_page = paginator.paginate_queryset(follow, request)
        serializer = FollowSerializer(
            recipes_page, many=True,
            context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request):
        serializer = PasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'detail': 'Пароль успешно изменен!'},
                        status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegistrationSerializer
        return UserSerializer


class TagViewSet(ListRetriveSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [ReadOnlyTag]


class IngredientViewSet(ListRetriveSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [permissions.AllowAny]
    filter_backends = (IngredientNameFilter, )
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet, CreateDestroyMixin):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PagePagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.create_сustom(
                request, FavoriteRecipe, FavoriteSerializer,
                obj_field='user', obj_id_field='recipe',
                obj=user, obj_id=recipe,
                error_message='Этот рецепт уже в избранном.')
        if request.method == 'DELETE':
            return self.destroy_сustom(
                request, FavoriteRecipe,
                obj_field='user', obj_id_field='recipe',
                obj=user, obj_id=recipe,
                detail_message='Рецепт успешно удален из избранного.')

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated],
            pagination_class=None)
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe_cart = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.create_сustom(
                request, ShoppingCartRecipe, ShoppingCartSerializer,
                obj_field='user', obj_id_field='recipe',
                obj=user, obj_id=recipe_cart,
                error_message='Этот рецепт уже в списке покупок.')
        if request.method == 'DELETE':
            return self.destroy_сustom(
                request, ShoppingCartRecipe,
                obj_field='user', obj_id_field='recipe',
                obj=user, obj_id=recipe_cart,
                detail_message='Рецепт успешно удален из списка покупок.')

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user

        ingredient_sum = RecipeIngredient.objects.filter(
            recipe__shoppingcartrecipe__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            amount_sum=Sum('amount')
        )

        file_list = []
        for ingredient in ingredient_sum:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount_sum = ingredient['total_amount']
            file_list.append(f"{name} - {amount_sum} {unit}.")

        content = 'Список покупок:\n' + '\n'.join(file_list)

        FILE_NAME = 'shopping_list.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{FILE_NAME}"'
        return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer
