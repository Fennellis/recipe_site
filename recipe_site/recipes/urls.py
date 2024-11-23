from django.urls import path
from .views import home, recipe_detail, add_recipe, user_login, user_register, logout_view, user_profile, edit_recipe

urlpatterns = [
    path('', home, name='home'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/edit/', edit_recipe, name='recipe_edit'),
    path('add_recipe/', add_recipe, name='add_recipe'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', user_profile, name='user_profile'),
]
