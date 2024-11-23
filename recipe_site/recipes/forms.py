from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description',
                  'instructions', 'preparation_time',
                  'image', 'ingredients', 'category']
