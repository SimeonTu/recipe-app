from django.forms import inlineformset_factory, ModelForm
from .models import Recipe, Ingredient, Step


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'difficulty', 'image']
        # Exclude any fields that shouldn't be filled out by the user, like an auto-generated slug field, if any.
        # Try excluding difficulty??


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('recipe',)


class StepForm(ModelForm):
    class Meta:
        model = Step
        exclude = ('recipe',)


IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=1, can_delete=True)
StepFormSet = inlineformset_factory(
    Recipe, Step, form=StepForm, extra=1, can_delete=True)
