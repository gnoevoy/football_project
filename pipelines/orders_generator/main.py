from pathlib import Path
import pandas as pd
import time
import sys

# Add python path
PIPELINES_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PIPELINES_DIR))

# Import helper functions
from orders_generator.db_helpers import get_max_order_id, get_products_with_sizes, load_to_postgre
from orders_generator.orders_helpers import generate_orders
from utils.logger import setup_logger


def orders_generator():
    try:
        # Set up logger
        LOGS_DIR = PIPELINES_DIR / "logs" / "orders_generator"
        logger = setup_logger(LOGS_DIR, "orders")

        t1 = time.perf_counter()
        logger.info("GENERATING ORDERS STARTED ..")

        # Generate orders and order details
        orders_num = 100
        order_id = get_max_order_id() + 1
        products = get_products_with_sizes()
        orders, order_details, order_details_num = generate_orders(orders_num, order_id, products)
        logger.info(f"Successfully created {orders_num} orders and {order_details_num} order details records")

        # Load data to PostgreSQL
        load_to_postgre(pd.DataFrame(orders), "orders")
        load_to_postgre(pd.DataFrame(order_details), "order_details")
        logger.info("Data succesffully loaded to database")

        # Log execution time
        t2 = time.perf_counter()
        logger.info(f"Script finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
    except:
        logger.error("", exc_info=True)
        raise


if __name__ == "__main__":
    orders_generator()
