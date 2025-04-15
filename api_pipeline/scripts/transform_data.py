import pandas as pd
import numpy as np
from pathlib import Path
import time
import sys
import ast

# add path path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# import helper functions
from functions.gcs_utils import get_file_from_bucket, load_file_to_bucket

# load json data (loop over two categories)

# get products with details (base df) -> create products tables
# get orders and order details (2 simple funciotns , loop over json data)

# in this file: load to bigquery + main logic with try-except
# in helpers all other functions


def get_products_with_details():
    df = pd.DataFrame()

    for category in ["boots", "balls"]:
        data = get_file_from_bucket("api-pipeline/raw", f"{category}.json", "json")
        category_id = 1 if category == "boots" else 2
        category_df = pd.json_normalize(data["products"])
        category_df["category_name"] = data["category_name"]
        category_df["category_id"] = category_id
        df = pd.concat([df, category_df], ignore_index=True)

    return df


def get_products(df):
    cols = ["product_id", "created_at", "title", "price", "old_price", "description", "avg_vote_rate", "num_votes", "category_id"]
    products = df[cols]
    products["description"] = products["description"].replace({None: np.nan})
    products["num_votes"] = products["num_votes"].astype("Int64")
    return products


def get_categories(df):
    categories = df[["category_id", "category_name"]].drop_duplicates()
    return categories


def get_labels(df):
    labels = df[["product_id", "labels"]]
    labels["labels"] = labels["labels"].apply(ast.literal_eval)
    labels = labels.explode("labels").dropna().rename(columns={"labels": "label"})
    labels["label"] = labels["label"].astype(str)
    return labels


def get_related_products(df):
    related_products = df[["product_id", "related_products"]]
    related_products["related_products"] = related_products["related_products"].apply(ast.literal_eval)
    related_products = related_products.explode("related_products").dropna().rename(columns={"related_products": "related_product_id"})
    related_products["related_product_id"] = related_products["related_product_id"].astype(int)
    return related_products


def get_sizes(df):
    pass


def get_features(df):
    pass


raise KeyError


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
