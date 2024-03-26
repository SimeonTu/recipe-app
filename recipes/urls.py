# recipes/urls.py
from django.urls import path
from .views import RecipeListView, RecipeDetailView, submit_recipe

app_name = 'recipes'

urlpatterns = [
    path('list/', RecipeListView.as_view(), name='list'),
    path('list/<pk>/', RecipeDetailView.as_view(), name='detail'),
    path('submit/', submit_recipe, name='submit_recipe'),
]
