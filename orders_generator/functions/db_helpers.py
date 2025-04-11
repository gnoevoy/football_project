from collections import defaultdict
from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import load_dotenv
from pathlib import Path
import sys
import os

# add python path and load variables
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

# postgres connection
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
SCHEMA = os.getenv("POSTGRES_SCHEMA")
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?options=-csearch_path%3D{SCHEMA}")


def get_max_order_id():
    with engine.connect() as conn:
        max_order_id = conn.execute(text("SELECT COALESCE(MAX(order_id), 0) FROM orders"))
        num = max_order_id.scalar()
    return num


def get_products_with_sizes():
    with engine.connect() as conn:
        products_query = conn.execute(text("SELECT product_id, price, old_price FROM products"))
        sizes_query = conn.execute(text("SELECT product_id, size FROM sizes WHERE in_stock = TRUE"))
        products = products_query.mappings().all()
        sizes = sizes_query.mappings().all()

    # get dct with product id's keys
    dct = defaultdict(dict)
    for product in products:
        product_id = product["product_id"]
        dct[product_id]["price"] = product["price"]
        dct[product_id]["old_price"] = product["old_price"]
        dct[product_id]["sizes"] = []

    # add sizes for each product
    for size in sizes:
        product_id = size["product_id"]
        dct[product_id]["sizes"].append(size["size"])

    # check for non empty sizes list for products
    dct = {k: v for k, v in dct.items() if v["sizes"]}
    return dct


def load_to_postgre(df, table_name):
    df.to_sql(table_name, engine, if_exists="append", index=False)
