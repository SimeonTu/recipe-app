from django.test import TestCase

from .models import Recipe, Ingredient


class RecipeModelTest(TestCase):
    # setting up non-modified objects used by test methods
    @classmethod
    def setUpTestData(cls):
        tea_recipe = Recipe.objects.create(
            name="Tea",
            cooking_time=5,
            instructions="Test instructions"
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
        self.assertEqual(recipe.get_absolute_url(), '/list/1')
