from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    cooking_time = models.IntegerField(help_text="Time in minutes")
    difficulty = models.CharField(max_length=50, default="TBA")
    image = models.ImageField(upload_to='recipes', default='no_image.jpg')
    description = models.TextField(help_text="Describe what the recipe is about.", default='N/A')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        # Check if the instance has a primary key (i.e., it has been saved)
        if self.pk is not None:
            
            # Determine the difficulty level based on cooking time and number of ingredients
            if self.cooking_time < 10 and self.ingredients.count() < 4:
                self.difficulty = "Easy"
            elif self.cooking_time < 10 and self.ingredients.count() >= 4:
                self.difficulty = "Medium"
            elif self.cooking_time >= 10 and self.ingredients.count() < 4:
                self.difficulty = "Intermediate"
            else:
                self.difficulty = "Hard"

        # Call the parent class's save method to save the changes
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients')
    quantity = models.CharField(
        max_length=100, blank=True, help_text="e.g., 1 tbsp (field not required)")
    name = models.CharField(max_length=255)
    description = models.CharField(
        max_length=255, blank=True, help_text="e.g., chopped, sliced (field not required)")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Capitalize the first letter of the ingredient's name
        self.name = self.name.capitalize()
        # Call the superclass's save method
        super().save(*args, **kwargs)


class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField()
    instructions = models.TextField()

    class Meta:
        # Ensure steps are ordered by their order attribute
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order} for {self.recipe.name}"
