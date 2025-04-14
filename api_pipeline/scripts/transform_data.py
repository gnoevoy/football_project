import pandas as pd
import numpy as np
from pathlib import Path
import time
import sys

# add path path and load variables
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# import helper functions
from functions.transform_helpers import load_products, get_products_and_sizes, get_orders_and_details
from functions.gcs_utils import get_file_from_bucket, load_file_to_bucket


# get orders and details
def get_orders_and_details():
    data = get_file_from_bucket("api-pipeline/raw", "orders.json", "json")
    orders = pd.DataFrame(data)
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["created_at"] = pd.to_datetime(orders["created_at"])

    # create order details table
    lst = []
    for _, row in orders[["order_id", "order_details"]].iterrows():
        if row["order_details"]:
            for detail in row["order_details"]:
                lst.append({"order_id": row["order_id"], **detail})

    order_details = pd.DataFrame(lst)
    orders.drop(columns=["order_details"], inplace=True)
    return orders, order_details


def transform_data(logger):
    try:
        t1 = time.perf_counter()
        logger.info("DATA TRANSFORMATION STARTED...")

        # main logic

        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
    except:
        logger.error(f"", exc_info=True)
