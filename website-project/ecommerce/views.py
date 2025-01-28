from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home_page(request):
    context = {"weapon": "p90"}
    return render(request, "ecommerce/home-page.html", context)
