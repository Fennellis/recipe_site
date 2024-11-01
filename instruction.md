Оглавление:
1. [Виртуальное окружение](#1)
2. [Модели](#models)

Создать и активировать виртуальное окружение
<a name="1"></a>
```
python -m venv <имя_окружения>
.\<имя_окружения>\Scripts\Activate.ps1
```

Установить Django
```
pip install django
```

Создать проект
```
django-admin startproject <имя_проекта>
```

Запуск сервера
```
python manage.py runserver <ip:port(опционально)>
```

В settings.py
```
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
 '127.0.0.1',
 '192.168.1.47',  # Адрес устройства, на котором запущен сервер
]
```

Создание приложения
```
python manage.py startapp <имя_приложения>
```

Добавить приложение в проект (settings.py)
```
INSTALLED_APPS = [
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 '<имя_приложения>',
]
```

Представление (в файл view.py)
```
from django.http import HttpResponse
from django.views import View

# Функциональное
def index(request):
 return HttpResponse("Hello, world!")

# Классовое
class HelloView(View):
def get(self, request):
    return HttpResponse("Hello World from class!")
```

Путь-базовый (в файл urls.py проекта)
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
 path('admin/', admin.site.urls),  # Путь админки
 path('', include('myapp.urls')),  # Базовый путь всех путей приложения
]
```

Путь-приложения (в файл urls.py приложения)
```
from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('about/', views.about, name='about'),
 path('posts/<int:year>/', year_post, name='year_post'), # Дополнительн передает параметр year в представление
]

_______________________________________

# name используется:
1) В шаблонах:
   <a href="{% url 'index' %}">Главная</a>
   <a href="{% url 'about' %}">О нас</a>

2) В представлениях:
    from django.urls import reverse
    from django.http import HttpResponseRedirect

    def some_view(request):
        return HttpResponseRedirect(reverse('about'))
    
    Здесь, когда вызывается `reverse('about')`,
    Django вернет URL, соответствующий маршруту с именем `about`.

3) В редиректах (перенаправлениях):
    from django.shortcuts import redirect

    def some_view(request):
        return redirect('index')
```

Логирование
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/path/to/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'myapp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,  # Передача родительским логерам
        },
    },
}

______________________________________

Пример:

import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def index(request):
    logger.info('Index page accessed')

Добавить форматирование:

'formatters': {
    'verbose': {
        'format': '{levelname} {asctime} {module} {process} {thread} {message}',
        'style': '{',
    },
    'simple': {
        'format': '%(levelname)s %(message)s'
    },
},

И добавить к handlers:

'console': {
    'class': 'logging.StreamHandler',
    'formatter': 'verbose', # добавлен параметр formatter
},

```

Модели (models.py)
```
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # Внешний ключ
```

Миграции
```
# Создать миграции в выбранном приложении (во всех если оставить пустым)

python manage.py makemigrations <имя_приложения>

# Применить миграции

python manage.py migrate
```

Свои команды
```
# Создать иерархию:

<my_project>/
    <my_app>/
        management(пакет)/
            commands(пакет)/
                <my_command>.py

______________________________________

# В <my_command>.py написать команду:

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Print 'Hello world!' to output."  # Выводится при передаче -h или --help параметра

    # Считать аргументы
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='User ID')

    def handle(self, *args, **kwargs):
        self.stdout.write('Hello world!')  # Вывод в стандартный поток Вв-Выв (консоль)

______________________________________

# Вызвать команду:

python manage.py my_comand
```

Создать объект модели
<a name="models"></a>
```
user = User(name='John', email='john@example.com', password='secret', age=25)
user.save()  # Сохранить в БД

ИЛИ

	
tom = Person.objects.create(name="Tom", age=23)  # Создать и добавить
person = await Person.objects.acreate(name="Tim", age=26)  # Для асинхронных функций

______________________________________


```

Получить объект модели
```
users = User.objects.all()  # Получить все объекты
self.stdout.write(f'{users}')

Или

pk = kwargs['pk']
user = User.objects.get(pk=pk) # Получить запись по указанному id (pk - primary key). Но вызовет ошибку, если записи не существует.

ИЛИ

author = get_object_or_404(Author, pk=author_id)  # Попытка получить объект. Если не существует - вызовет страницу с ошибкой 404 (можно обработать свою или использовать страницу по умолчанию)

Или

user = User.objects.filter(age__gt=age).first()  # Вернуть все объекты, подходящие под фильтр и выбрать первый из них. None если ничего не нашли.
```

Обновить объект модели
```
pk = kwargs.get('pk')
name = kwargs.get('name')
user = User.objects.filter(pk=pk).first()
user.name = name  # Обновили имя
user.save()  # Сохранили обновленную запись
```

Удалить объект модели
```
pk = kwargs.get('pk')
user = User.objects.filter(pk=pk).first()
if user is not None:
    user.delete()
```

Связи таблиц
```
1) Один ко многим (Один автор - много постов)
class Author(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')

# С помощью related_name можно обратиться
# ко всем постам автора через  author_posts = author.posts.all()

2) Многие ко многим (Много категорий - много постов)
class Category(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    authors = models.ManyToManyField(Author, related_name='posts')
    categories = models.ManyToManyField(Category, related_name='posts')

3) Один к одному (Один автор - один профиль)
class Author(models.Model):
    name = models.CharField(max_length=100)

class AuthorProfile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    website = models.URLField()
```

Шаблоны
```
myproject/
    myapp1/
        templates/
            myapp1/
                index.html
    myapp2/
        templates/
            myapp2/
                index.html
    myproject/
    manage.py
```

Базовый шаблон
```
myproject/
    myapp/
        ...
    manage.py
    templates/
        base.html
        
+

В файл settings.py найти TEMPLATES и добавить в список DIRS путь:

BASE_DIR / 'templates'

Теперь можно наследовать шаблоны без явного указания пути родителя:

{% extends 'base.html' %}
```