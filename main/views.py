import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from .models import Employee

from .models import Product
from .forms import ProductForm

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'app_name': 'MiuFootball Shop',
        'name': '2406428876 - Khayra Tazkiya',
        'class_name': 'PBP D',
        'product_list': Product.objects.all(),
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, 'main.html', context)

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_product.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def show_xml(request):
    data = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(data, content_type='application/xml')

def show_json(request):
    products = Product.objects.all().select_related('user')
    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "thumbnail": p.thumbnail,
            "category": p.category,
            "is_featured": p.is_featured,
            "stock": p.stock,
            "brand": p.brand,
            "user_id": p.user_id,
            # kalau ada created_at: "created_at": p.created_at.isoformat() if p.created_at else None,
        } for p in products
    ]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    data = serializers.serialize("xml", [product])
    return HttpResponse(data, content_type='application/xml')

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'content': product.content,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'product_views': product.product_views,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user_id else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_main')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, id):
    return render(request, "product_detail.html", {"product":get_object_or_404(Product, pk=id)})

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# bikin satu function baru di views, namanya add_employee, untuk nambahin satu Employee baru dengan field:
# name nya nama kamu, age nya bebas, persona nya bebas
#return nya pakai HttpResponse aja biar keliatan

def add_employee(request):
    emp =  Employee.objects.create(
    name = "Khayra Tazkiya",
    age = 18,
    persona = "Pacil",
    )

    return HttpResponse("employee berhasil dibuat")

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.increment_views()

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    # Ambil data dari form (nama field dari frontend)
    name = request.POST.get("name", "").strip()              # -> Product.name
    content = request.POST.get("content", "").strip()          # -> Product.description
    price = request.POST.get("price", "").strip()              # WAJIB
    category = request.POST.get("category", "").strip()
    thumbnail = request.POST.get("thumbnail", "").strip() or "https://via.placeholder.com/150"
    is_featured = request.POST.get("is_featured") in ("on", "true", "1")
    stock = request.POST.get("stock", "0").strip()
    brand = request.POST.get("brand", "").strip()

    # Sanitasi sederhana biar aman dari XSS text
    name = strip_tags(name)
    content = strip_tags(content)
    brand = strip_tags(brand)
    category = strip_tags(category)

    # Validasi minimal
    if not name or not price:
        return JsonResponse({"detail": "Nama (title) dan price wajib diisi."}, status=400)

    try:
        price = int(price)
        stock = int(stock or 0)
    except ValueError:
        return JsonResponse({"detail": "price/stock harus berupa angka."}, status=400)

    # Simpan ke model Product (peta field yang benar)
    product = Product.objects.create(
        name=name,
        description=content,
        price=price,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        stock=stock,
        brand=brand,
        user=request.user if request.user.is_authenticated else None,
    )

    # Balikkan JSON supaya frontend bisa refresh tanpa reload
    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "thumbnail": product.thumbnail,
        "is_featured": product.is_featured,
        "stock": product.stock,
        "brand": product.brand,
        "user_id": product.user_id,
    }, status=201)