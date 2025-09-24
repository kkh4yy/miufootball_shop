from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers

from .models import Product
from .forms import ProductForm


def show_main(request):
    context = {
        'app_name': 'MiuFootball Shop',
        'name': '2406428876 - Khayra Tazkiya',
        'class_name': 'PBP D',
        'product_list': Product.objects.all()
    }

    return render(request, 'main/main.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():  
            form.save()
            return redirect('main:show_main')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def show_xml(request):
    data = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(data, content_type='application/xml')

def show_json(request):
    data = serializers.serialize("json", Product.objects.all())
    return HttpResponse(data, content_type='application/json')

def show_xml_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    data = serializers.serialize("xml", [product])
    return HttpResponse(data, content_type='application/xml')

def show_json_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    data = serializers.serialize("json", [product])
    return HttpResponse(data, content_type='application/json')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_main')
    else:
        form = ProductForm()
    return render(request, 'main/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/product_list.html', {'products': products})

def product_detail(request, id):
    return render(request, "main/product_detail.html", {"product":get_object_or_404(Product, pk=id)})

