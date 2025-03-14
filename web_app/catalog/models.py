# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "categories"


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    category_id = models.IntegerField()
    scraped_id = models.IntegerField(unique=True)
    url = models.TextField()
    created_at = models.DateTimeField()
    title = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    avg_vote_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    num_votes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "products"


class Colors(models.Model):
    product = models.ForeignKey("Products", models.DO_NOTHING)
    color = models.IntegerField()

    class Meta:
        managed = False
        db_table = "colors"
        unique_together = (("product", "color"),)


class Images(models.Model):
    product = models.ForeignKey("Products", models.DO_NOTHING)
    image = models.TextField()
    is_thumbnail = models.BooleanField()

    class Meta:
        managed = False
        db_table = "images"
        unique_together = (("product", "image", "is_thumbnail"),)


class Labels(models.Model):
    product = models.ForeignKey("Products", models.DO_NOTHING)
    label = models.TextField()

    class Meta:
        managed = False
        db_table = "labels"
        unique_together = (("product", "label"),)


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    order_date = models.DateTimeField()
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "orders"


class OrderDetails(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey("Orders", models.DO_NOTHING)
    product = models.ForeignKey("Products", models.DO_NOTHING)
    quantity = models.IntegerField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "order_details"


class Sizes(models.Model):
    product = models.ForeignKey(Products, models.DO_NOTHING)
    size = models.TextField()
    in_stock = models.BooleanField()

    class Meta:
        managed = False
        db_table = "sizes"
        unique_together = (("product", "size", "in_stock"),)


class Summary(models.Model):
    record_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField()
    total = models.IntegerField()
    new_boots = models.IntegerField(blank=True, null=True)
    new_balls = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "summary"
