from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User
from reviews.models import (Tag, Recipe, Ingredient, RecipeIngredient,
                            FavoriteRecipe, Follow, ShoppingCartRecipe)


from .utils import (IngredientNameFilter, PagePagination, RecipeFilter)
from .mixins import ListRetriveSet, CreateListRetriveSet
from .permissions import ReadOnlyTag
from .serializers import (TagSerializer, RecipeReadSerializer,
                          RecipeCreateSerializer, FollowSerializer,
                          IngredientSerializer, UserSerializer,
                          PasswordSerializer, UserRegistrationSerializer,
                          FavoriteSerializer, ShoppingCartSerializer)


class UserViewSet(CreateListRetriveSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'],
            # permission_classes=[permissions.IsAuthenticated]
            )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk):
        user = self.request.user
        if request.method == 'POST':
            author = get_object_or_404(User, id=pk)
            if author == user:
                return Response(
                    {'error': 'Вы не можете подписаться на себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'error': 'Вы уже подписаны на этого пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(follow, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            author = get_object_or_404(User, id=pk)
            get_object_or_404(Follow, user=request.user,
                              author=author).delete()
            return Response(
                {'detail': 'Успешная отписка'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PagePagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    # def get_queryset(self):
    #     queryset = Recipe.objects.all()
    #     favorite_recipes = FavoriteRecipe.objects.all()
    #     cart_recipes = ShoppingCartRecipe.objects.all()
    #     user = self.request.user
    #     params = self.request.query_params
    #     print(params)
    # if 'is_in_shopping_cart' in params:
    #     queryset = cart_recipes.filter(user=user)
    #     return queryset
    # if 'is_favorited' in params:
    #     queryset = favorite_recipes.filter(user=user)
    #     return queryset
    # return queryset

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if FavoriteRecipe.objects.filter(user=user,
                                             recipe=recipe).exists():
                return Response(
                    {'error': 'Этот рецепт уже в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST)
            favorite = FavoriteRecipe.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(
                favorite, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(FavoriteRecipe, user=request.user,
                              recipe=recipe).delete()
            return Response({'detail': 'Рецепт успешно удален из избранного.'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated],
            pagination_class=None)
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe_cart = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if ShoppingCartRecipe.objects.filter(user=user,
                                                 recipe=recipe_cart).exists():
                return Response(
                    {'error': 'Этот рецепт уже в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST)
            recipe_cart = ShoppingCartRecipe.objects.create(
                user=user, recipe=recipe_cart)
            serializer = ShoppingCartSerializer(
                recipe_cart, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(ShoppingCartRecipe, user=request.user,
                              recipe=recipe_cart).delete()
            return Response({'detail': 'Рецепт успешно удален из покупок.'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        recipes_cart = ShoppingCartRecipe.objects.filter(
            user=user).values_list('recipe', flat=True)
        ingredients = RecipeIngredient.objects.filter(
            recipe__in=recipes_cart)

        ingredient_sum = {}

        for ingredient in ingredients:
            name = ingredient.ingredient.name
            unit = ingredient.ingredient.measurement_unit
            amount = ingredient.amount

            key = (name, unit)

            if key in ingredient_sum:
                ingredient_sum[key] += amount
            else:
                ingredient_sum[key] = amount

        file_list = []
        for (name, unit), total_amount in ingredient_sum.items():
            file_list.append(f"{name} - {total_amount} {unit}.")

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
