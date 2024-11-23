from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from .forms import RecipeForm
import random


def home(request):
    all_recipes = list(Recipe.objects.all())
    random_recipes = random.sample(all_recipes, min(len(all_recipes), 5))

    return render(request, 'recipes/home.html', {'recipes': random_recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})


def edit_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user != recipe.author:
            return redirect('recipe_detail', recipe_id=recipe_id)
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.pk)
        return render(request,
                      'recipe_edit.html',
                      {'form': form, 'recipe': recipe})
    else:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user != recipe.author:
            return redirect('recipe_detail', recipe_id=recipe_id)
        form = RecipeForm(instance=recipe)
        return render(request,
                      'recipes/recipe_edit.html',
                      {'form': form, 'recipe': recipe})

# class RecipeEditView(View):
#     def get(self, request, pk):
#         recipe = get_object_or_404(Recipe, pk=pk)
#         if request.user != recipe.author:
#             return redirect('recipe_detail', pk=pk)  # Перенаправить, если не автор
#         form = RecipeForm(instance=recipe)  # Предварительно заполняем форму
#         return render(request, 'your_app_name/recipe_edit.html', {'form': form, 'recipe': recipe})
#
#     def post(self, request, pk):
#         recipe = get_object_or_404(Recipe, pk=pk)
#         if request.user != recipe.author:
#             return redirect('recipe_detail', pk=pk)  # Перенаправить, если не автор
#         form = RecipeForm(request.POST, request.FILES, instance=recipe)
#         if form.is_valid():
#             form.save()
#             return redirect('recipe_detail', pk=recipe.pk)  # Перенаправление на страницу рецепта
#         return render(request, 'your_app_name/recipe_edit.html', {'form': form, 'recipe': recipe})


def user_profile(request, user_id):
    # Получаем пользователя по его ID
    user = get_object_or_404(User, id=user_id)

    # Получаем все рецепты, принадлежащие этому пользователю
    recipes = Recipe.objects.filter(author=user)  # Замените 'author' на ваше поле, связывающее рецепт с пользователем

    # Передаем данные в шаблон
    return render(request, 'user/profile.html', {
        'user': user,
        'recipes': recipes,
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Неправильное имя пользователя или пароль.'})
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
