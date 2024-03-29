from django.test import TestCase, Client
from django.urls import reverse
from .forms import IngredientFormSet, RecipeForm, RecipeSearchForm
from .models import Recipe, Ingredient
from django.contrib.auth.models import User

class RecipeModelTest(TestCase):
    # setting up non-modified objects used by test methods
    @classmethod
    def setUpTestData(cls):
        tea_recipe = Recipe.objects.create(
            name="Tea",
            cooking_time=5,
            description="Test description."
        )

        # Create Ingredient objects and link them to the Recipe object
        Ingredient.objects.create(
            recipe=tea_recipe,
            quantity="1 cup",
            name="Water",
            description=""
        )
        Ingredient.objects.create(
            recipe=tea_recipe,
            quantity="1 tsp.",
            name="Sugar",
            description=""
        )
        Ingredient.objects.create(
            recipe=tea_recipe,
            quantity="1",
            name="Tea Bag",
            description=""
        )

    def test_name_length(self):
        # get recipe to test
        recipe = Recipe.objects.get(id=1)
        # get metadata of name field and use to query its max_length
        max_length = recipe._meta.get_field("name").max_length
        # compare value to expected result
        self.assertEqual(max_length, 255)

    def test_name_label(self):
        recipe = Recipe.objects.get(id=1)
        # get metadata of name field and use to query its label
        recipe_name_label = recipe._meta.get_field("name").verbose_name
        # compare value to expected result
        self.assertEqual(recipe_name_label, "name")

    def test_name(self):
        recipe = Recipe.objects.get(id=1)
        # compare name value to expected result
        self.assertEqual(recipe.name, "Tea")

    def test_cooking_time(self):
        recipe = Recipe.objects.get(id=1)
        # compare cooking time value to expected result
        self.assertEqual(recipe.cooking_time, 5)

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        # get_absolute_url() should take you to the detail page of recipe #1
        # and load the URL /recipes/list/1
        self.assertEqual(recipe.get_absolute_url(), '/recipes/list/1/')

    def test_view_uses_correct_template(self):
        """Check the template used by the Recipe list view."""
        response = self.client.get(
            reverse('recipes:list'))  # Use the name you've given the URL in your urls.py
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')


class RecipeFormTest(TestCase):

    def test_recipe_form_valid(self):
        """Test RecipeForm with valid data"""
        form_data = {
            'name': 'New Recipe',
            'cooking_time': 30,
            'difficulty': 'Medium',
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid(self):
        """Test RecipeForm with invalid data"""
        # Assuming 'name' is required
        form_data = {
            'cooking_time': 15,
            # Missing 'name'
            'difficulty': 'Easy',
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class RecipeSearchFormTest(TestCase):

    def test_recipe_search_form_valid(self):
        """Test RecipeSearchForm with valid data including optional fields."""
        form_data = {
            'name': 'Some Recipe',
            'difficulty': 'Easy',
            'cooking_time': '10-20',
            # ingredients is omitted since it's optional and requires a bit more setup
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class IngredientFormSetTest(TestCase):

    def test_ingredient_formset_valid(self):
        """Test valid submission of multiple ingredients via the formset."""
        recipe = Recipe.objects.create(
            name="Test Recipe", cooking_time=20, difficulty="Medium")
        formset_data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-name': 'Flour',
            'ingredients-0-quantity': '2 cups',
            'ingredients-0-description': 'All-purpose',
        }
        formset = IngredientFormSet(data=formset_data, instance=recipe)
        self.assertTrue(formset.is_valid(), formset.errors)
        formset.save()
        self.assertEqual(recipe.ingredients.count(), 1)

# Ensure proper template usage, context data, and form handling for RecipeListView, RecipeDetailView, and the submit_recipe.

from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe, Ingredient
from .forms import RecipeForm

class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

class RecipeListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        for i in range(3):
            Recipe.objects.create(name=f'Recipe {i}', cooking_time=10+i, difficulty='Easy')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/list/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')

class RecipeDetailViewTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(name='Test Recipe', cooking_time=15, difficulty='Medium')

    def test_view_status_code(self):
        url = reverse('recipes:detail', args=[self.recipe.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('recipes:detail', args=[self.recipe.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/recipes_detail.html')

class SubmitRecipeTest(TestCase):
    def test_recipe_creation_view(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        response = self.client.get("/recipes/submit/")
        self.assertEqual(response.status_code, 200)

        post_response = self.client.post("/recipes/submit/", {
            'name': 'Test Recipe',
            'cooking_time': 20,
            'difficulty': 'Easy',
        })
