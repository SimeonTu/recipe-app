from django.forms import inlineformset_factory, ModelForm
from django import forms
from .models import Recipe, Ingredient, Step
from django_select2.forms import Select2MultipleWidget, Select2Widget


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

def iformat():
    return '${<i class="fa fa-camera-retro fa-lg"></i>}'

class RecipeSearchForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search for recipes'}))

    difficulty = forms.ChoiceField(choices=[('', 'Difficulty'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Intermediate', 'Intermediate'), ('Hard', 'Hard')], required=False,
                                   widget=Select2Widget(attrs={'class': 'form-select', 'data-minimum-results-for-search': 'Infinity'}))

    cooking_time = forms.ChoiceField(choices=[('', 'Cooking Time'), ('1-10', '1-10 mins'), ('10-20', '10-20 mins'), ('20-30', '20-30 mins'), ('30-40', '30-40 mins'),
                                     ('40-50', '40-50 mins'), ('50-60', '50-60 mins'), ('60+', '60+ mins')], required=False,
                                     widget=Select2Widget(attrs={'class': 'form-select',  'data-minimum-results-for-search': 'Infinity'}))

    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=Select2MultipleWidget(
        attrs={'class': 'form-control form-select select2-multi', 'data-maximum-selection-length': "3"}), required=False)
