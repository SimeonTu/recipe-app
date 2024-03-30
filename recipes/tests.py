from .forms import RecipeSearchForm
from .forms import IngredientForm, StepForm
from .forms import RecipeForm
from django.test import TestCase, Client
from django.urls import reverse
from .forms import IngredientFormSet, RecipeForm, RecipeSearchForm, LoginForm, RegisterForm
from .models import Recipe, Ingredient, Step
from django.contrib.auth.models import User

# Views test cases

class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home')) 
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

class RecipeListViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create test recipes
        self.recipe1 = Recipe.objects.create(
            name="Chocolate Cake",
            cooking_time=45,
            difficulty="Medium",
            description="Delicious chocolate cake.",
            submitted_on="2023-03-29",
            submitted_by=self.user
        )
        self.recipe2 = Recipe.objects.create(
            name="Spaghetti Carbonara",
            cooking_time=30,
            difficulty="Easy",
            description="Tasty and easy spaghetti carbonara.",
            submitted_on="2023-03-30",
            submitted_by=self.user
        )

        # Create ingredients related to the recipes
        Ingredient.objects.create(recipe=self.recipe1, name="Chocolate", quantity="100g")
        Ingredient.objects.create(recipe=self.recipe2, name="Spaghetti", quantity="200g")

    def test_recipe_list_view_no_filter(self):
        response = self.client.get(reverse('recipes:list'))  # Adjust as per your URL name
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.recipe1, response.context['recipe_list'])
        self.assertIn(self.recipe2, response.context['recipe_list'])

    def test_recipe_list_view_name_filter(self):
        response = self.client.get(reverse('recipes:list'), {'name': 'chocolate'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.recipe1, response.context['recipe_list'])
        self.assertNotIn(self.recipe2, response.context['recipe_list'])

class RecipeDetailViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create a test recipe
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            cooking_time=20,
            difficulty="Easy",
            description="This is a test recipe.",
            submitted_by=self.user
        )

        # Optionally, create related ingredients and steps
        Ingredient.objects.create(
            recipe=self.recipe,
            quantity="2 cups",
            name="Flour",
            description="sifted"
        )
        
        Step.objects.create(
            recipe=self.recipe,
            order=1,
            instructions="Mix all dry ingredients."
        )
        
        # More ingredients or steps can be added similarly

    def test_detail_view_with_existing_recipe(self):
        # Now, use self.recipe.id to construct the URL for the detail view test
        response = self.client.get(reverse('recipes:detail', args=(self.recipe.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_detail.html')

        # You can also assert that the context contains the correct recipe
        self.assertEqual(response.context['recipe'].id, self.recipe.id)
        self.assertEqual(response.context['recipe'].name, "Test Recipe")



# Forms test cases
class LoginFormTestCase(TestCase):
    def test_login_form_valid_data(self):
        form = LoginForm(data={'username': 'testuser', 'password': '12345'})
        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        # Expecting errors for both fields
        self.assertEqual(len(form.errors), 2)


class RegisterFormTestCase(TestCase):
    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            'username': 'testuser',
            'email': 'user@example.com',
            'password1': 'Testpass123',
            'password2': 'Testpass123'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        # Expecting errors for missing fields
        self.assertEqual(len(form.errors), 4)


class RecipeFormTestCase(TestCase):
    def test_recipe_form_valid_data(self):
        form = RecipeForm(data={
            'name': 'Test Recipe',
            'cooking_time': 30,
            'description': 'Test Description'
            # Assume 'image' and 'difficulty' are optional or provide valid data here.
        })
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid_data(self):
        form = RecipeForm(data={})
        # Depending on your model constraints, adjust the expected errors
        self.assertFalse(form.is_valid())


class IngredientFormTestCase(TestCase):
    def test_ingredient_form_valid_data(self):
        # Assuming 'name' is a required field in your model
        form = IngredientForm(data={'name': 'Flour'})
        self.assertTrue(form.is_valid())


class StepFormTestCase(TestCase):
    def test_step_form_valid_data(self):
        # Assuming 'description' is a required field in your model
        form = StepForm(data={'order': '1', 'instructions': 'test'})
        self.assertTrue(form.is_valid())


class RecipeSearchFormTestCase(TestCase):
    def setUp(self):
        # If you're using real model instances, ensure you have some Ingredients created
        pass

    def test_recipe_search_form_valid_data(self):
        form = RecipeSearchForm(data={
            'name': 'Test',
            'difficulty': 'Easy',
            # 'cooking_time' and 'ingredients' can also be tested similarly
        })
        self.assertTrue(form.is_valid())
