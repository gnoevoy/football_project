import pandas as pd
import numpy as np
from pathlib import Path
import time
import sys

# add path path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# import helper functions
from functions.gcs_utils import get_file_from_bucket, load_file_to_bucket


# featch category table
def get_category_table(raw_files_dir, category):
    data = get_file_from_bucket(raw_files_dir, f"{category}.json", "json")
    df = pd.DataFrame(data["products"])
    df["category_name"] = data["category_name"]
    return df


def get_products(logger):
    categories = ["boots", "balls"]
    raw_files_dir = "api-pipeline/raw"
    products = pd.DataFrame()

    # construct one table from multiple categories
    for category in categories:
        df = get_category_table(raw_files_dir, category)
        products = pd.concat([products, df], ignore_index=True)

    # clean products table
    products["category_id"] = np.where(products["category_name"] == "boots", 1, 2)
    products["description"] = products["description"].apply(lambda value: value if value else np.nan)
    logger.info("Products table successfully created and processed")
    return products


# get order details from each order
def process_order_details(data):
    lst = []
    for order in data:
        order_id = order["order_id"]
        details = [{"order_id": order_id, **detail} for detail in order["order_details"]]
        lst.extend(details)
        order.pop("order_details")
    return pd.DataFrame(lst)


def get_orders_and_details(logger):
    raw_files_dir = "api-pipeline/raw"
    data = get_file_from_bucket(raw_files_dir, f"orders.json", "json")
    order_details = process_order_details(data)
    orders = pd.DataFrame(data)
    logger.info("Orders and Order Details tables successfully created and processed")
    return orders, order_details


def load_files(products, orders, order_details, logger):
    clean_files_dir = "api-pipeline/clean"
    load_file_to_bucket(products, clean_files_dir, "products.csv", "csv")
    load_file_to_bucket(orders, clean_files_dir, "orders.csv", "csv")
    load_file_to_bucket(order_details, clean_files_dir, "order_details.csv", "csv")
    logger.info("Files successfully loaded to GCS bucket")


# logic: get category tables and create products table -> get orders and order details -> load files to GCS bucket
def transform_data(logger):
    try:
        t1 = time.perf_counter()
        logger.info("DATA TRANSFORMATION STARTED...")

        products = get_products(logger)
        orders, order_details = get_orders_and_details(logger)
        load_files(products, orders, order_details, logger)

        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
    except:
        logger.error(f"", exc_info=True)
