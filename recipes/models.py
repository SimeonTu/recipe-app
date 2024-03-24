from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=50, help_text="50 characters max")
    ingredients = models.CharField(max_length=255, help_text="255 characters max, separated by commas; ex: banana, milk")  
    cooking_time = models.IntegerField(help_text="In minutes")
    instructions = models.TextField(help_text="Instructions for making the recipe")


    def calculate_difficulty(self):
        ingredients = self.ingredients.split(',')
        if self.cooking_time < 30 and len(ingredients) < 6:
            return 'Easy'
        elif self.cooking_time < 30 and len(ingredients) >= 6:
            return 'Medium'
        elif self.cooking_time >= 30 and len(ingredients) < 6:
            return 'Intermediate'
        elif self.cooking_time >= 30 and len(ingredients) >= 6:
            return 'Hard'
        return 'difficulty'
    
    def __str__(self):
        return str(self.name)