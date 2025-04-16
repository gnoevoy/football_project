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
    get_categories,
    get_labels,
    get_related_products,
    get_sizes,
    get_features,
    get_orders_and_details,
)

clean_files_dir = "api-pipeline/clean"


def process_and_load_products_data(product_ids, logger):
    df, is_empty = get_products_with_details(product_ids)
    if not is_empty:
        products = get_products(df)
        categories = get_categories(df)
        labels = get_labels(df)
        related_products = get_related_products(df)
        sizes = get_sizes(df)
        features = get_features(df)
        logger.info("Products data successfully processed")

        # write tables to bucket
        load_file_to_bucket(products, clean_files_dir, "products.csv", "csv")
        load_file_to_bucket(categories, clean_files_dir, "categories.csv", "csv")
        load_file_to_bucket(labels, clean_files_dir, "labels.csv", "csv")
        load_file_to_bucket(related_products, clean_files_dir, "related_products.csv", "csv")
        load_file_to_bucket(sizes, clean_files_dir, "sizes.csv", "csv")
        load_file_to_bucket(features, clean_files_dir, "features.csv", "csv")
        logger.info("Files successfully loaded to bucket")

        new_products = True
        return new_products
    else:
        logger.info("No new products")
        new_products = False
        return new_products


def process_and_load_orders_data(order_ids, logger):
    orders, order_details = get_orders_and_details(order_ids)

    if len(orders) > 0:
        logger.info("Orders data successfully processed")
        load_file_to_bucket(orders, clean_files_dir, "orders.csv", "csv")
        load_file_to_bucket(order_details, clean_files_dir, "order_details.csv", "csv")
        logger.info("Files successfully loaded to bucket")
        new_orders = True
        return new_orders
    else:
        logger.info("No new orders")
        new_orders = False
        return new_orders


# logic: get category tables and create products table -> get orders and order details -> load files to GCS bucket
def transform_data(logger):
    try:
        t1 = time.perf_counter()
        logger.info("DATA TRANSFORMATION STARTED ...")

        # get data from bigquery to filter out data
        product_ids, order_ids = get_products_and_orders_ids()
        new_products = process_and_load_products_data(product_ids, logger)
        new_orders = process_and_load_orders_data(order_ids, logger)

        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
        return new_products, new_orders
    except:
        logger.error(f"", exc_info=True)
