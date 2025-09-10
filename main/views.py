
# Create your views here.
from django.shortcuts import render

def show_main(request):
    context = {
        'app_name': 'MiuFootball Shop',
        'name': '2406428876 - Khayra Tazkiya',
        'class_name': 'PBP D'
    }
    return render(request, 'main.html', context)