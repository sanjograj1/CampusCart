from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import ProductForm, ProductFilterForm
from .models import Product

from django.contrib import messages


@login_required
def home(request):
    if request.method == "GET":
        form = ProductFilterForm(request.GET)
        if form.is_valid():
            category = form.cleaned_data.get("category")
            search = form.cleaned_data.get("search")
            if category and search:
                products = Product.objects.filter(
                    category__iexact=category, title__icontains=search
                )
            elif category:
                products = Product.objects.filter(category__iexact=category)
            elif search:
                products = Product.objects.filter(title__icontains=search)
            else:
                products = Product.objects.all()
    else:

        products = Product.objects.all()

    return render(request, "products/home.html", {"products": products, "form": form})


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

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


# detail product
@login_required
def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_interested = product.is_interested(request.user)

    return render(
        request,
        "products/product_detail.html",
        {"product": product, "is_interested": is_interested},
    )


# add user to interested users for a product
@login_required
def interested_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.interested_users.add(request.user)
    print("product", product.id)
    messages.add_message(
        request,
        messages.SUCCESS,
        "You have successfully added to interested users list !!",
        extra_tags="success",
    )
    return redirect("products:detail_product", pk=product.id)


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.user:
        return redirect(
            "home"
        )  # Or some other appropriate response for unauthorized access
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:home")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/edit_product.html", {"form": form})
