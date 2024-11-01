from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

class HomeView(View):
    def get(self, request) -> HttpResponse:
        return render(request, 'main_part/home.html', context={})