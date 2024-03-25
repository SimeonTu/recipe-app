from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

# Create your views here.


def home(request):
    # Define a list of the specific recipe names you want
    featured_recipes = ["Tea", "Scrambled Eggs", "Banana Pancakes", "Tomato Basil Pasta"]
    
    # Filter recipes whose name is in the specific_names list
    specific_recipes = Recipe.objects.filter(name__in=featured_recipes)
    
    # Pass the filtered recipes to the template
    return render(request, 'recipes/recipes_home.html', {'recipes': specific_recipes})

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'


class RecipeDetailView(DetailView):      # class-based view
    model = Recipe                       # specify model
    template_name = 'recipes/recipes_detail.html'  # specify template
