from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Recipe
from .forms import IngredientFormSet, StepFormSet, RecipeForm

# Create your views here.

# Home page
def home(request):
    # Define a list of the specific recipe names you want
    featured_recipes = ["Tea", "Scrambled Eggs",
                        "Banana Pancakes", "Tomato Basil Pasta"]

    # Filter recipes whose name is in the specific_names list
    specific_recipes = Recipe.objects.filter(name__in=featured_recipes)

    # Pass the filtered recipes to the template
    return render(request, 'recipes/recipes_home.html', {'recipes': specific_recipes})

# All recipes list page
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'

# Specific recipe details page
class RecipeDetailView(DetailView):      # class-based view
    model = Recipe                       # specify model
    template_name = 'recipes/recipes_detail.html'  # specify template

# Records/Stats page
def records(request):
   #do nothing, simply display page    
   return render(request, 'recipes/records.html')

# Login-protected page that lest users submit new recipes to the site
@login_required
def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            # If your Recipe model has an author or similar field:
            # recipe.author = request.user
            ingredientFormSet = IngredientFormSet(request.POST, instance=recipe)
            stepFormSet = StepFormSet(request.POST, instance=recipe)
            if ingredientFormSet.is_valid() and stepFormSet.is_valid():
                # Use a database transaction to ensure that saving the recipe and its related
                # ingredients and steps either all succeed together or all fail together. This
                # prevents partial saves and maintains data integrity by rolling back all changes
                # if any part of the operation fails.
                with transaction.atomic():
                    recipe.save()  # First, save the Recipe object
                    ingredientFormSet.save()  # Then save the related objects
                    stepFormSet.save()
                return redirect('home')
    else:
        form = RecipeForm()
        ingredientFormSet = IngredientFormSet()
        stepFormSet = StepFormSet()
    return render(request, 'recipes/recipes_create.html', {'form': form, 'ingredientFormSet': ingredientFormSet, 'stepFormSet': stepFormSet})