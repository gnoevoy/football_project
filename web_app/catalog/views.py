from django.shortcuts import render
from .models import Products, Categories, Colors, Sizes, Labels, Images


# Create your views here.
def home(request):
    return render(request, "catalog/home.html")


def catalog(request, category):
    category_id_obj = Categories.objects.filter(category_name=category).values("category_id").first()

    products = Products.objects.filter(category_id=category_id_obj["category_id"]).values("product_id", "title", "price", "old_price")

    context = {"category": category, "products": products, "x": category_id_obj["category_id"]}
    return render(request, "catalog/catalog.html", context)


def product_page(request, id):
    return render(request, "catalog/product-page.html")
