from django.shortcuts import render
from django.utils.text import slugify
from django.http import HttpResponse
from .models import (
    Categories,
    Product,
    Colors,
    Sizes,
    Labels,
    Product_Images,
    Boots_Features,
    Balls_Features,
)

# Create your views here.


def home(request):
    categories = Categories.objects.all()
    new_products = Product.objects.filter(labels__label_name="New").order_by("-price")[
        :4
    ]

    for product in new_products:
        print(product.name)

    context = {"categories": categories, "new_products": new_products}
    return render(request, "ecommerce/home-page.html", context)


def catalog(request, category_name):
    products = Product.objects.filter(category_id__category_name=category_name)
    context = {"products": products}
    return render(request, "ecommerce/catalog.html", context)


def product_page(request, category_name, product_slug, pk):

    return HttpResponse("product page")
