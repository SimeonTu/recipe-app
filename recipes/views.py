from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg
from .models import Recipe
from .forms import IngredientFormSet, StepFormSet, RecipeForm, RecipeSearchForm
import pandas as pd
from .utils import get_chart1, get_chart2

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
    dataframes = None   #initialize dataframe to None
    chart1 = None
    chart_difficulty = None

    def get_queryset(self):
        queryset = super().get_queryset()

        self.form = RecipeSearchForm(self.request.GET or None)

        if self.form.is_valid():
            name = self.form.cleaned_data.get('name')
            difficulty = self.form.cleaned_data.get('difficulty')
            cooking_time_choice = self.form.cleaned_data.get('cooking_time')
            ingredients = self.form.cleaned_data.get('ingredients')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if difficulty and difficulty != '':
                queryset = queryset.filter(difficulty=difficulty)

            # Handle the cooking time choice
            if cooking_time_choice:
                if cooking_time_choice != '60+ mins':  # Handle all cases except '60+ mins'
                    # Split the choice to get the min and max time
                    min_time, max_time = map(
                        int, cooking_time_choice.split('-'))
                    queryset = queryset.filter(
                        cooking_time__gte=min_time, cooking_time__lte=max_time)
                else:  # Handle '60+ mins'
                    queryset = queryset.filter(cooking_time__gte=60)

            if ingredients:
                queryset = queryset.filter(
                    ingredients__in=ingredients).distinct()
            
            # average cooking time by difficulty level
            queryset_difficulty = Recipe.objects.values('difficulty').annotate(average_cooking_time=Avg('cooking_time')).order_by('difficulty')

            dataframes_difficulty = pd.DataFrame(queryset_difficulty)

            # order of these are important!
            self.dataframes = pd.DataFrame(queryset.values()) # convert queryset to panda dataframes

            self.chart1 = get_chart1(self.dataframes) # call get_chart by passing panda dataframes
            self.chart_difficulty = get_chart2(dataframes_difficulty)

            self.dataframes = self.dataframes.to_html(classes=["table", "table-striped", "table-hover"], index=False) # convert dataframes to HTML

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form  # Add the form to the context
        context['sales_df'] = self.dataframes
        context['chart1'] = self.chart1
        context['chart_difficulty'] = self.chart_difficulty

        return context

# Specific recipe details page


class RecipeDetailView(DetailView):      # class-based view
    model = Recipe                       # specify model
    template_name = 'recipes/recipes_detail.html'  # specify template

# Records/Stats page


@login_required
def records(request):
    # do nothing, simply display page
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
            ingredientFormSet = IngredientFormSet(
                request.POST, instance=recipe)
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
