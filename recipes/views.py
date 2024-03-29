from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.contrib import messages
from .models import Recipe, Ingredient
from .forms import IngredientFormSet, StepFormSet, RecipeForm, RecipeSearchForm
import pandas as pd
from .utils import bar_chart_recipe_number_by_difficulty, pie_chart_recipes_by_cooking_time, line_chart_ingredient_usage, categorize_cooking_times

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

    df_search_results = None
    chart_recipe_number_by_difficulty = None
    chart_cooking_times_ranges = None
    chart_ingredient_usage = None

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

            # convert search result recipes queryset into dataframes
            # convert queryset to panda dataframes
            self.df_search_results = pd.DataFrame(queryset.values())

            # Distribution of recipes by cooking time range
            qs_cooking_time_ranges = queryset.values_list(
                'cooking_time', flat=True)
            categorized_cooking_times = categorize_cooking_times(
                qs_cooking_time_ranges)
            df_cooking_time_ranges = pd.DataFrame(list(categorized_cooking_times.items()), columns=[
                                                  'Cooking Time Range', 'Number of Recipes'])

            # Number of recipes that use each existing ingredient
            # Filter ingredients by the filtered recipes queryset
            filtered_ingredients = Ingredient.objects.filter(
                recipe__in=queryset)
            qs_ingredient_usage = filtered_ingredients.values(
                'name').annotate(total=Count('name')).order_by('-total')
            df_ingredient_usage = pd.DataFrame(qs_ingredient_usage)

            # get chart image from each chart function by passing it the dataframes
            self.chart_recipe_number_by_difficulty = bar_chart_recipe_number_by_difficulty(
                self.df_search_results)
            self.chart_cooking_times_ranges = pie_chart_recipes_by_cooking_time(
                df_cooking_time_ranges)
            self.chart_ingredient_usage = line_chart_ingredient_usage(
                df_ingredient_usage)

            # search results dataframes converted into an HTML table
            self.df_search_results = self.df_search_results.to_html(
                classes=["table", "table-striped", "table-hover"], index=False)  # convert dataframes to HTML

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form  # Add the form to the context
        context['df_search_results'] = self.df_search_results
        context['chart_recipe_number_by_difficulty'] = self.chart_recipe_number_by_difficulty
        context['chart_cooking_times_ranges'] = self.chart_cooking_times_ranges
        context['chart_ingredient_usage'] = self.chart_ingredient_usage

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

                messages.success(
                    request, 'You have successfully submitted a recipe.')

                return redirect('recipes:list')
    else:
        form = RecipeForm()
        ingredientFormSet = IngredientFormSet()
        stepFormSet = StepFormSet()
    return render(request, 'recipes/recipes_create.html', {'form': form, 'ingredientFormSet': ingredientFormSet, 'stepFormSet': stepFormSet})
