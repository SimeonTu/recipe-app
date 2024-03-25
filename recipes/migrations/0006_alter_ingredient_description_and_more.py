# Generated by Django 5.0.3 on 2024-03-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='description',
            field=models.CharField(blank=True, help_text='e.g., chopped, sliced (field not required)', max_length=255),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.CharField(blank=True, help_text='e.g., 1 tbsp (field not required)', max_length=100),
        ),
    ]
