from django.urls import path, include

from rest_framework import routers


from .views import (TagViewSet, RecipeViewSet,
                    IngredientViewSet, UserViewSet)


router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagViewSet)
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
