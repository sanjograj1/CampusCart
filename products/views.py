from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from notifications.signals import notify
from .forms import ProductForm, ProductFilterForm
from .models import Product
from django.contrib.auth import get_user_model

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
                print(products[0].description)
    else:

        products = Product.objects.all()

    return render(request, "products/home.html", {"products": products, "form": form,'title':'Products'})


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.errors, dir(form))
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            sender = get_user_model().objects.get(username=request.user)
            receiver = get_user_model().objects.exclude(username=request.user)
            description = f'<b>{product.title}</b> ({product.category}). Click <a href="/product/detail-product/{product.id}">here</a> to view.'
            notify.send(sender, recipient=receiver, verb='Upload', description=description)
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
        {"product": product, "is_interested": is_interested,'title':product.title},
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
def edit_product(request, productid):
    my_product = get_object_or_404(Product, pk=productid)
    if my_product.user != request.user:
        messages.success(request, "You don't have the access to the Product",extra_tags='danger')
        return redirect('accounts:user-listing')
    if request.method == 'POST':
        if 'action' in request.POST:
            form = ProductForm(request.POST,request.FILES, instance=my_product)
            if form.is_valid():
                book = form.save(commit=False)
                book.save()
                return redirect('accounts:user-listing')
        else:
            my_product.delete()
            messages.success(request, "Your Product has been deleted",extra_tags='danger')
            return redirect('accounts:user-listing')
    else:    
        form = ProductForm(instance=my_product)
    return render(request, 'products/edit_product.html',{
        'form': form,
        'title':'Edit Product'
        })
