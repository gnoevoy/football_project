from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify


# Create your models here.


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name="products",
        db_column="category_id",
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(blank=True, null=True)
    scraped_num = models.IntegerField(unique=True)
    scraped_link = models.URLField(unique=True)
    created_at = models.DateTimeField(default=now)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class Colors(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="colors", db_column="product_id"
    )
    color_name = models.CharField(max_length=50)

    def __str__(self):
        return self.product_id


class Sizes(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sizes", db_column="product_id"
    )
    size_num = models.CharField(max_length=20)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.product_id


class Labels(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="labels", db_column="product_id"
    )
    label_name = models.CharField(max_length=100)

    def __str__(self):
        return self.product_id


class Product_Images(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", db_column="product_id"
    )
    image_name = models.CharField(max_length=255)
    is_thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return self.product_id


class Balls_Features(models.Model):
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="balls_features",
        db_column="product_id",
    )
    producer = models.CharField(max_length=100, null=True, blank=True)
    ball_size = models.CharField(max_length=100, null=True, blank=True)
    ground_type = models.CharField(max_length=100, null=True, blank=True)
    class_type = models.CharField(max_length=100, null=True, blank=True)
    collection = models.CharField(max_length=100, null=True, blank=True)
    connecting_type = models.CharField(max_length=100, null=True, blank=True)
    weight = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    manufacturers_data = models.CharField(max_length=100, null=True, blank=True)
    league = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.product_id


class Boots_Features(models.Model):
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="boots_features",
        db_column="product_id",
    )
    producer = models.CharField(max_length=100, null=True, blank=True)
    collections = models.CharField(max_length=100, null=True, blank=True)
    age_group = models.CharField(max_length=100, null=True, blank=True)
    ground_type = models.CharField(max_length=100, null=True, blank=True)
    class_type = models.CharField(max_length=100, null=True, blank=True)
    upper = models.CharField(max_length=100, null=True, blank=True)
    type_of_binding = models.CharField(max_length=100, null=True, blank=True)
    boots_with_sock = models.CharField(max_length=100, null=True, blank=True)
    collection_name = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    plays_in_these_boots = models.CharField(max_length=100, null=True, blank=True)
    manufacturers_data = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.product_id
