from pathlib import Path
import sys
import random
import pandas as pd
import traceback

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

# generate orders and order details
try:
    for _ in range(orders_num):
        order = generate_order(order_id)
        num_products = random.randint(1, 2)
        order_products = random.sample(list(products.keys()), num_products)

        for product in order_products:
            order_detail = generate_order_detail(order_id, products, product)
            order_details.append(order_detail)

        orders.append(order)
        order_id += 1

    print("Data successfully generates")

except Exception:
    traceback.print_exc()

# write data to database
try:
    orders_df = pd.DataFrame(orders)
    order_details = pd.DataFrame(order_details)
    load_to_db(orders_df, "orders")
    load_to_db(order_details, "order_details")
    print("Data successfully written into db")

except Exception:
    traceback.print_exc()
