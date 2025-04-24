from collections import defaultdict
from sqlalchemy import text
from pathlib import Path
import sys

# Add python path
PIPELINES_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PIPELINES_DIR))

# Import db engine
from utils.connections import engine


# Retrieve highest order_id from db
def get_max_order_id():
    with engine.connect() as conn:
        max_order_id = conn.execute(text("SELECT COALESCE(MAX(order_id), 0) FROM orders"))
        num = max_order_id.scalar()
    return num


# Retrieve necessaty data for generating orders
def get_products_with_sizes():
    with engine.connect() as conn:
        products_query = conn.execute(text("SELECT product_id, price, old_price FROM products"))
        sizes_query = conn.execute(text("SELECT product_id, size FROM sizes WHERE in_stock = TRUE"))
        products = products_query.mappings().all()
        sizes = sizes_query.mappings().all()

    # Construct a dct with product_id as key
    dct = defaultdict(dict)
    for product in products:
        product_id = product["product_id"]
        dct[product_id]["price"] = product["price"]
        dct[product_id]["old_price"] = product["old_price"]
        dct[product_id]["sizes"] = []

    # Add sizes for each product
    for size in sizes:
        product_id = size["product_id"]
        dct[product_id]["sizes"].append(size["size"])

    # Check for non empty sizes list
    dct = {k: v for k, v in dct.items() if v["sizes"]}
    return dct


def load_to_postgre(df, table_name):
    df.to_sql(table_name, engine, if_exists="append", index=False)
