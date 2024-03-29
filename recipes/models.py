from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.



class Recipe(models.Model):
    name = models.CharField(max_length=255)
    cooking_time = models.IntegerField(help_text="Time in minutes")
    difficulty = models.CharField(max_length=50, default="Unknown")
    image = models.ImageField(upload_to='recipes', default='no_image.jpg')
    description = models.TextField(
        max_length=480, help_text="Describe what the recipe is about. Max 480 characters", default='N/A')
    # Automatically set the field to now when the object is first created.
    submitted_on = models.DateTimeField(auto_now_add=True)
    # Using Django's built-in User model
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})

    def update_difficulty(self):
        if self.cooking_time < 10 and self.ingredients.count() < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and self.ingredients.count() >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and self.ingredients.count() < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def save(self, *args, **kwargs):

        # Check if the instance has a primary key (i.e., it has been saved)
        if self.pk is not None:

            # Determine the difficulty level based on cooking time and number of ingredients
            self.update_difficulty()

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

@receiver(post_save, sender=Ingredient)
@receiver(post_delete, sender=Ingredient)
def update_recipe_difficulty_on_ingredient_change(sender, instance, **kwargs):
    if instance.recipe_id:
        recipe = Recipe.objects.get(id=instance.recipe_id)
        recipe.update_difficulty()
        recipe.save()