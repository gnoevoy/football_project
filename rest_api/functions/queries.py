from collections import defaultdict
from sqlalchemy import text
from pathlib import Path
import sys

# Add python path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# Import connections
from functions.connections import engine, mongo_collection


# Retrieve product sizes
def get_sizes(db, product_ids):
    sizes_query = db.execute(text("SELECT * FROM sizes WHERE product_id IN :product_ids"), {"product_ids": tuple(product_ids)})
    sizes = sizes_query.mappings().all()
    dct = defaultdict(lambda: {"in_stock": [], "out_of_stock": []})

    # Add sizes to the dct
    for size in sizes:
        product_id = size["product_id"]
        if size["in_stock"]:
            dct[product_id]["in_stock"].append(size["size"])
        else:
            dct[product_id]["out_of_stock"].append(size["size"])
    return dct


# Retrieve product details from MongoDB
def get_product_details(product_id):
    details = mongo_collection.find_one({"_id": product_id})
    details.pop("_id")
    details.pop("product_id")
    return details


# Display products for a given category
def display_products(category_name):
    dct = {"category_name": category_name, "products": []}
    category_id = 1 if category_name == "boots" else 2

    with engine.connect() as db:
        # Query the database for products in the given category
        products_query = db.execute(text("SELECT * FROM products WHERE category_id = :category_id"), {"category_id": category_id})
        products = products_query.mappings().all()
        product_ids = [product["product_id"] for product in products]

        # Get sizes
        sizes = get_sizes(db, product_ids)

    # Compose product records with core info, sizes, and additional details from MongoDB
    for product in products:
        row = {**product}
        row["sizes"] = sizes[row["product_id"]]
        details = get_product_details(row["product_id"])
        row["labels"] = details["labels"]
        row["related_products"] = details["related_products"]
        row["features"] = details["features"]

        # Remove unnecessary fields from the record
        for key in ["scraped_id", "url", "category_id"]:
            row.pop(key)
        dct["products"].append(row)

    return dct


# Retrieve order details in a structured format grouped by order ID
def get_order_details_dct(db):
    order_details_query = db.execute(text("SELECT * FROM order_details"))
    order_details = order_details_query.mappings().all()
    dct = defaultdict(list)

    for order_detail in order_details:
        row = {**order_detail}
        order_id = row["order_id"]
        row.pop("order_id")
        dct[order_id].append(row)
    return dct


# Display all orders with their details
def display_orders():
    with engine.connect() as db:
        # Query the database for all orders
        orders_query = db.execute(text("SELECT * FROM orders"))
        orders = orders_query.mappings().all()
        order_details = get_order_details_dct(db)

    # Compose order records with their details
    lst = []
    for order in orders:
        row = {**order}
        row["order_details"] = order_details[row["order_id"]]
        row.pop("created_at")
        lst.append(row)

    return lst
