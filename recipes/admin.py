from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Recipe, Ingredient, Step

# Inline admin for Ingredients
class IngredientInline(admin.TabularInline):
    model = Ingredient
    # This determines how many blank ingredient forms are shown by default.
    extra = 1

# Inline admin for Steps
class StepInline(admin.TabularInline):
    model = Step
    # This determines how many blank step forms are shown by default.
    extra = 1

# Admin model for Recipe
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # Customize the list display
    list_display = ('name', 'cooking_time', 'difficulty')
    # Add StepInline to allow adding steps from the admin panel
    inlines = [IngredientInline, StepInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # After the main instance and related objects have been saved, perform the custom validation
        recipe_instance = form.instance
        if not recipe_instance.ingredients.exists():
            # Use the messages framework to provide a user-friendly error message
            messages.error(
                request, 'The recipe must have at least one ingredient.')
        if not recipe_instance.steps.exists():
            # Use the messages framework to provide a user-friendly error message
            messages.error(request, 'The recipe must have at least one step.')
