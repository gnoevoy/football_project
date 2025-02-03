from django.contrib import admin
from .models import (
    Categories,
    Product,
    Colors,
    Sizes,
    Labels,
    Product_Images,
    Balls_Features,
    Boots_Features,
)

# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Colors)
admin.site.register(Sizes)
admin.site.register(Labels)
admin.site.register(Product_Images)
admin.site.register(Balls_Features)
admin.site.register(Boots_Features)
