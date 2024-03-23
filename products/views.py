from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from notifications.signals import notify
from .forms import ProductForm, ProductFilterForm
from .models import Product, ProductViews
from django.contrib.auth import get_user_model

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal


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

            paginator = Paginator(products, 9)

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
    else:

        products = Product.objects.all()

    return render(
        request,
        "products/home.html",
        {"products": products, "form": form, "title": "Products",'page_obj':page_obj},
    )


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
            notify.send(
                sender, recipient=receiver, verb="Upload", description=description
            )
            return redirect("products:home")
    else:
        form = ProductForm()
    return render(request, "products/create_product.html", {"form": form})


# detail product
@login_required
def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_interested = product.is_interested(request.user)
    # get similer products based on category of product
    similar_products = Product.objects.filter(category=product.category).exclude(
        id=product.id
    )[:4]
    # see other product in same price range where price difference is less than 10%
    same_price_products = Product.objects.filter(
        price__gte=Decimal(product.price) * Decimal("0.5"),
        price__lte=Decimal(product.price) * Decimal("1.5"),
    ).exclude(id=product.id)[:4]
    product_view = ProductViews.objects.filter(user_session_key=request.session.session_key, product=product)
    if not product_view.exists():
        ProductViews.objects.create(product=product, user=request.user, user_session_key=request.session.session_key)
    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "is_interested": is_interested,
            "title": product.title,
            "similar_products": similar_products,
            "same_price_products": same_price_products,
        },
    )


# add user to interested users for a product
@login_required
def interested_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user in product.interested_users.all():
        product.interested_users.remove(request.user)
        message = "You have been removed from the interested users list."
    else:
        product.interested_users.add(request.user)
        message = "You have been added to the interested users list."
    messages.success(request, message, extra_tags="success")
    return redirect("products:detail_product", pk=product.id)


@login_required
def edit_product(request, productid):
    my_product = get_object_or_404(Product, pk=productid)
    if my_product.user != request.user:
        messages.success(
            request, "You don't have the access to the Product", extra_tags="danger"
        )
        return redirect("accounts:user-listing")
    if request.method == "POST":
        if "action" in request.POST:
            form = ProductForm(request.POST, request.FILES, instance=my_product)
            if form.is_valid():
                book = form.save(commit=False)
                book.save()
                return redirect("accounts:user-listing")
        else:
            my_product.delete()
            messages.success(
                request, "Your Product has been deleted", extra_tags="danger"
            )
            return redirect("accounts:user-listing")
    else:
        form = ProductForm(instance=my_product)
    return render(
        request, "products/edit_product.html", {"form": form, "title": "Edit Product"}
    )
