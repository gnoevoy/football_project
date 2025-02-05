from django.shortcuts import render
from django.db.models import OuterRef, Subquery
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

product_images_prefix = (
    "https://storage.cloud.google.com/football_project/ecommerce/product-images/"
)


def home(request):
    categories = Categories.objects.all()
    new_products = Product.objects.filter(labels__label="new").select_related(
        "category_id"
    )

    context = {
        "categories": categories,
        "new_products": new_products,
        "img_prefix": product_images_prefix,
    }
    return render(request, "ecommerce/home-page.html", context)


def catalog(request, category):
    # category = Categories.objects.get(category_name=category)
    products = Product.objects.filter(category_id__category_name=category)

    context = {
        "category": category,
        "products": products,
        "img_prefix": product_images_prefix,
    }
    return render(request, "ecommerce/catalog.html", context)


def product_page(request, category, slug, pk):
    category = Categories.objects.get(category_name=category)
    product = Product.objects.get(product_id=pk)

    context = {"category": category, "product": product}
    return render(request, "ecommerce/product-page.html", context)
