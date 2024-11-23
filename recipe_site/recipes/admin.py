from django.contrib import admin

from recipes.models import RecipeCategory, Recipe, Category


# Register your models here.

class RecipeCategoryInline(admin.TabularInline):
    model = RecipeCategory
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'preparation_time')
    search_fields = ('title', 'author__username')
    list_filter = ('category',)
    inlines = [RecipeCategoryInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
