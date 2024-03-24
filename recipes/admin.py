from django.contrib import admin

# Import the recipes model
from .models import Recipe 

# Register your models here.
admin.site.register(Recipe)