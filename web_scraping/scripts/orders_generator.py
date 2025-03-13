from pathlib import Path
import sys
import random
import pandas as pd

# Set base path for helper functions
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))


# Import helper functions
from utils.logger import setup_logger
from web_scraping.functions.db_helpers import order_generetor_queries, load_to_db
from web_scraping.functions.orders_helpers import generate_order, generate_order_detail

try:
    # Set up logger for script
    LOGS_DIR = ROOT_DIR / "logs" / "orders_generator"
    logger = setup_logger(LOGS_DIR / f"orders.log")

    orders, order_details = [], []
    orders_num = random.randint(1, 3)
    max_order_id, products = order_generetor_queries()
    order_id = max_order_id + 1

    # generate orders and order details
    for _ in range(orders_num):
        order = generate_order(order_id)
        num_products = random.randint(1, 2)
        order_products = random.sample(list(products.keys()), num_products)

        for product in order_products:
            order_detail = generate_order_detail(order_id, products, product)
            order_details.append(order_detail)

        orders.append(order)
        order_id += 1

    logger.info("Data successfully generates")

    # write data to database
    orders_df = pd.DataFrame(orders)
    order_details = pd.DataFrame(order_details)
    load_to_db(orders_df, "orders")
    load_to_db(order_details, "order_details")

    logger.info("Data successfully written into db")
    logger.info("-------------------------------------------------------")

except Exception:
    logger.error(f"Unexpected error", exc_info=True)
    logger.info("-------------------------------------------------------")
