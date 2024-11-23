from django.db import models
from django.contrib.auth.models import User
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField()
    preparation_time = models.IntegerField()
    image = models.ImageField(upload_to='recipes/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.TextField(blank=True)
    category = models.ManyToManyField(Category, through='RecipeCategory', blank=True)

    def __str__(self):
        return self.title

    def get_category_display(self):
        if self.category.exists():
            return ', '.join([cat.name for cat in self.category.all()])
        return "Не указано"


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description',
                  'instructions', 'preparation_time',
                  'image', 'ingredients', 'category']


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
