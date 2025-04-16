from google.cloud import bigquery
from dotenv import load_dotenv
from pathlib import Path
import time
import sys
import os

# add python path and load variables
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

# import helper functions
from functions.utils import load_table_to_bigquery

BUCKET_URL = os.getenv("BUCKET_URL")
BIGQUERY_PATH = os.getenv("WAREHOUSE_SCHEMA")


def load_product_tables(new_products, logger):
    product_tables = ["features", "labels", "products", "related_products", "sizes"]
    if new_products:
        for table in product_tables:
            gcs_url = f"{BUCKET_URL}/{table}.csv"
            table_id = f"{BIGQUERY_PATH}.{table}"
            load_table_to_bigquery(gcs_url, table_id)
            logger.info(f"{table.title()} successfully loaded to BigQuery")
    else:
        logger.info("No new products")


def load_order_tables(new_orders, logger):
    order_tables = ["orders", "order_details"]
    if new_orders:
        for table in order_tables:
            gcs_url = f"{BUCKET_URL}/{table}.csv"
            table_id = f"{BIGQUERY_PATH}.{table}"
            load_table_to_bigquery(gcs_url, table_id)
            logger.info(f"{table.title()} successfully loaded to BigQuery")
    else:
        logger.info("No new orders")


def load_data(new_products, new_orders, logger):
    try:
        t1 = time.perf_counter()
        logger.info("LOADING DATA STARTED...")

        load_product_tables(new_products, logger)
        load_order_tables(new_orders, logger)

        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
    except:
        logger.error(f"", exc_info=True)
