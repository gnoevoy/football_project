from .connections import engine, mongo_collection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from collections import defaultdict

# map existing database tables to ORM classes
Base = automap_base()
Base.prepare(autoload_with=engine)
Products = Base.classes.products
Categories = Base.classes.categories
Sizes = Base.classes.sizes
Orders = Base.classes.orders
OrderDetails = Base.classes.order_details


# helper to creates dctionary with sizes
def get_sizes_dct(sizes):
    dct = defaultdict(lambda: {"in_stock": [], "out_of_stock": []})
    for size in sizes:
        size_data = {"size": size.size, "in_stock": size.in_stock}
        if size.in_stock:
            dct[size.product_id]["in_stock"].append(size_data["size"])
        else:
            dct[size.product_id]["out_of_stock"].append(size_data["size"])
    return dct


# helper to query mongodb and get product details
def get_product_details(product_id):
    details = mongo_collection.find_one({"_id": product_id})
    details.pop("_id")
    details.pop("product_id")
    return details


def get_product_data(product, sizes_dct):
    product_data = product.__dict__
    product_id = product_data["product_id"]

    # add sizes and product details to record
    product_data["sizes"] = sizes_dct[product_id]
    details_dct = get_product_details(product_id)
    product_data.update(details_dct)

    # remove unnecessary data
    for key in ["_sa_instance_state", "scraped_id", "url", "category_id"]:
        product_data.pop(key)

    return product_data


def display_products(category_name):
    dct = {"category_name": category_name, "products": []}
    category_id = 1 if category_name == "boots" else 2

    with Session(engine) as db:
        # get category products
        products = db.query(Products).filter(Products.category_id == category_id)
        product_ids = [product.product_id for product in products.all()]

        # get sizes
        sizes = db.query(Sizes).filter(Sizes.product_id.in_(product_ids))
        sizes_dct = get_sizes_dct(sizes)

    # loop over products and add core info, sizes and details
    for product in products:
        product_data = get_product_data(product, sizes_dct)
        dct["products"].append(product_data)

    return dct


# helper to create dictionary with order details
def get_order_details_dct(order_details):
    dct = defaultdict(list)

    for detail in order_details:
        data = detail.__dict__
        order_id = data["order_id"]
        for key in ["_sa_instance_state", "order_id", "order_detail_id"]:
            data.pop(key)
        dct[order_id].append(data)

    return dct


def display_orders():
    lst = []

    with Session(engine) as db:
        # get orders with details
        orders = db.query(Orders)
        order_details = db.query(OrderDetails)
        details = get_order_details_dct(order_details)

    # loop over orders and add data
    for order in orders:
        order_data = order.__dict__
        order_id = order_data["order_id"]
        order_data["order_details"] = details[order_id]

        # remove unnecessary data
        for key in ["_sa_instance_state", "created_at"]:
            order_data.pop(key)
        lst.append(order_data)

    return lst
