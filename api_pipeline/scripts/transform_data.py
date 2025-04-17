from pathlib import Path
import time
import sys

# add path path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# import helper functions
from functions.utils import load_file_to_bucket
from functions.transform_helpers import (
    get_products_and_orders_ids,
    get_products_with_details,
    get_products,
    get_labels,
    get_related_products,
    get_sizes,
    get_features,
    get_orders_and_details,
)

CLEAN_FILES_DIR = "api-pipeline/clean"


# handle products data
def products_wrapper(products_ids, logger):
    df = get_products_with_details(products_ids)
    logger.info("Produts data successfully extracted")

    if len(df) > 0:
        products = get_products(df)
        labels = get_labels(df)
        related_products = get_related_products(df)
        sizes = get_sizes(df)
        features = get_features(df)

        # load dataframes to bucket + logs
        load_file_to_bucket(products, CLEAN_FILES_DIR, "products.csv", "csv")
        logger.info(f"Products successfully loaded to bucket, {len(products)} records")
        load_file_to_bucket(labels, CLEAN_FILES_DIR, "labels.csv", "csv")
        logger.info(f"Labels successfully loaded to bucket, {len(labels)} records")
        load_file_to_bucket(related_products, CLEAN_FILES_DIR, "related_products.csv", "csv")
        logger.info(f"Related products successfully loaded to bucket, {len(related_products)} records")
        load_file_to_bucket(sizes, CLEAN_FILES_DIR, "sizes.csv", "csv")
        logger.info(f"Sizes successfully loaded to bucket, {len(sizes)} records")
        load_file_to_bucket(features, CLEAN_FILES_DIR, "features.csv", "csv")

        # boolean needs to determine if new data, if so in the next ETL step we will load it to warehouse
        return True
    else:
        logger.info("No new products found")
        return False


# handle orders data
def orders_wrapper(order_ids, logger):
    orders, order_details = get_orders_and_details(order_ids)
    logger.info("Orders data successfully extracted")

    if len(orders) > 0:
        load_file_to_bucket(orders, CLEAN_FILES_DIR, "orders.csv", "csv")
        logger.info(f"Orders successfully loaded to bucket, {len(orders)} records")
        load_file_to_bucket(order_details, CLEAN_FILES_DIR, "order_details.csv", "csv")
        logger.info(f"Order details successfully loaded to bucket, {len(order_details)} records")

        # the same logic as for products
        return True
    else:
        logger.info("No new orders found")
        return False


def transform_data(logger):
    try:
        t1 = time.perf_counter()
        logger.info("DATA TRANSFORMATION STARTED ...")

        # get ids from bigquery to prevent loading already existed data to warehouse
        product_ids, order_ids = get_products_and_orders_ids()
        new_products = products_wrapper(product_ids, logger)
        new_orders = orders_wrapper(order_ids, logger)

        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
        return new_products, new_orders
    except:
        logger.error(f"", exc_info=True)
