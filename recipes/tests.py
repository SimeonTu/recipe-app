from django.test import TestCase

from .models import Recipe


class RecipeModelTest(TestCase):
    # setting up non-modified objects used by test methods
    def setUpTestData():
        Recipe.objects.create(
            name="Tea",
            cooking_time=5,
            ingredients=["Water", "Sugar", "Tea Leaves"],
            instructions="Test instructions"
        )

    def test_name_length(self):
        # get recipe to test
        recipe = Recipe.objects.get(id=1)
        # get metadata of name field and use to query its max_length
        max_length = recipe._meta.get_field("name").max_length
        # compare value to expected result
        self.assertEqual(max_length, 50)

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

    def test_ingredients_help_text(self):
        recipe = Recipe.objects.get(id=1)
        # get metadata of ingredients field and use to query its help text
        ing_help_text = recipe._meta.get_field("ingredients").help_text
        # compare value to expected result
        self.assertEqual(ing_help_text, "255 characters max, separated by commas; ex: banana, milk")