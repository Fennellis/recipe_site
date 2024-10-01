from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cooking_time = models.DurationField()
    image = models.ImageField(upload_to='recipes/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class CookingSteps(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField('steps/')
