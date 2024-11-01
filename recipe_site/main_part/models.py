from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class RecipeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    steps = models.TextField()
    cooking_time = models.IntegerField()
    picture = models.ImageField(upload_to='recipes/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    category = models.ManyToManyField(RecipeCategory, related_name='recipes')


class RecipeSteps(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='recipe_steps/')
