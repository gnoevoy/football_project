from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:category>/", views.catalog, name="catalog"),
    path(
        "<str:category>/<slug:slug>:<int:pk>",
        views.product_page,
        name="product-page",
    ),
]
