# Generated by Django 5.0.3 on 2024-03-24 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('ingredients', models.CharField(max_length=500)),
                ('cooking_time', models.IntegerField()),
                ('instructions', models.TextField()),
            ],
        ),
    ]
