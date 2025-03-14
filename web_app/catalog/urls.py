from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:category>/", views.catalog, name="catalog"),
    path("item/<int:id>", views.product_page, name="product-page"),
]
