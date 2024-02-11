from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product


@login_required
def home(request):
    products = Product.objects.all()

    return render(request, "products/home.html", {"products": products})


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        print("form valid", form.errors)
        if form.is_valid():
            print(form.errors, dir(form))
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            print("product", product.id)
            return redirect("products:home")
    else:
        form = ProductForm()
    return render(request, "products/create_product.html", {"form": form})


