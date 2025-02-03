from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:category_name>/", views.catalog, name="catalog"),
    path(
        "<str:category_name>/<str:product_slug>:<int:pk>",
        views.product_page,
        name="product-page",
    ),
]
