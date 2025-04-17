from pathlib import Path
import pandas as pd
import logging
import time

# Import helper functions
from functions.db_helpers import get_max_order_id, get_products_with_sizes, load_to_postgre
from functions.orders_helpers import generate_orders


def setup_logger():
    LOG_FILE_PATH = Path(__file__).parent / "orders.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d_%H:%M:%S",
        filename=LOG_FILE_PATH,
        filemode="w",
    )
    return logging.getLogger()


def main(orders_num):
    try:
        t1 = time.perf_counter()
        logger = setup_logger()
        logger.info("GENERATING ORDERS STARTED ..")

        # Generate orders and order details
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


if __name__ == "__main__":
    main(100)
