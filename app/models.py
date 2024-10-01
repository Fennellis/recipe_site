from django.db import models

# Create your models here.


class Recipe(models.Model):
    title = models.CharField()
    description = models.TextField()
    steps = models.Field()
    cooking_time = models.TimeField()
    image = models.ImageField
    author = models.ForeignKey()
