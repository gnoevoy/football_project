from pathlib import Path
import sys
import random
from datetime import datetime, timedelta
import pandas as pd

# Set base path for helper functions
base_path = Path.cwd() / "web-scraping"
sys.path.append(str(base_path))

# Import helper functions
from functions.db_helpers import order_generetor_queries, load_to_db
from functions.orders_helpers import generate_order, generate_order_detail

orders, order_details = [], []

orders_num = random.randint(1, 3)
max_order_id, products = order_generetor_queries()
order_id = max_order_id + 1

first_day = datetime(datetime.now().year, datetime.now().month, 1)
last_day = datetime(datetime.now().year, datetime.now().month + 1, 1) - timedelta(days=1)

# generate orders and order details
try:
    for _ in range(orders_num):
        order = generate_order(order_id, first_day, last_day)
        num_products = random.randint(1, 2)
        order_products = random.sample(list(products.keys()), num_products)
        order_detail_id = 1

        for product in order_products:
            order_detail = generate_order_detail(order_detail_id, products, product)
            order_details.append(order_detail)
            order_detail_id += 1

        orders.append(order)
        order_id += 1

except Exception:
    ...


# write data to database
try:
    orders_df = pd.DataFrame(orders)
    order_details = pd.DataFrame(order_details)
    load_to_db(orders_df, "orders")
    load_to_db(order_details, "order_details")


except Exception:
    ...


from pprint import pprint

pprint(orders)
pprint(order_details)
