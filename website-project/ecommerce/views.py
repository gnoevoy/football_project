from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.


def home_page(request):
    lst = [i for i in range(4, 13)]
    context = {"length": lst}
    return render(request, "ecommerce/home-page.html", context)


def output(request):
    length = int(request.GET.get("len", 8))
    letters = "abcdefjh"
    output = "".join([random.choice(letters) for i in range(length)])

    context = {"output": output}
    return render(request, "ecommerce/output.html", context)
