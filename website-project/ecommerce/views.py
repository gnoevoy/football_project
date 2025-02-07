from django.shortcuts import render
from django.db.models import Count
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
    # categories
    categories_lst = list(
        Categories.objects.annotate(products_count=Count("products"))
        .order_by("category_id")
        .values("category_name", "products_count")
    )
    preview_img = [
        "https://storage.cloud.google.com/football_project/ecommerce/website-images/balls-preview.jpg",
        "https://storage.cloud.google.com/football_project/ecommerce/website-images/boots-preview.jpg",
    ]
    for i, category in enumerate(categories_lst):
        category["preview_img"] = preview_img[i]

    # new products (at the moment all products)
    new_products = (
        Product.objects.all().select_related("category_id").prefetch_related("labels")
    )

    context = {
        "categories": categories_lst,
        "new_products": new_products,
    }
    return render(request, "ecommerce/home-page.html", context)


def catalog(request, category):
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
