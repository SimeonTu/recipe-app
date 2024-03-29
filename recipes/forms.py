from django.forms import inlineformset_factory, ModelForm
from django import forms
from .models import Recipe, Ingredient, Step
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import FormActions

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login', css_class='btn-primary mt-3')
        )

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Add a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'password1',
            'password2',
            Submit('submit', 'Register', css_class='btn-primary mt-3')
        )


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'image']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('cooking_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'difficulty',
            'image',
            FormActions(
                Submit('save', 'Submit Recipe', css_class='btn-primary')
            )
        )


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('recipe',)


class StepForm(ModelForm):
    class Meta:
        model = Step
        exclude = ('recipe',)


IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=1, can_delete=False)
StepFormSet = inlineformset_factory(
    Recipe, Step, form=StepForm, extra=1, can_delete=False)


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
