from dotenv import load_dotenv
from pathlib import Path
import time
import sys
import os

# Add python path and load variables
PIPELINES_DIR = Path(__file__).parents[2]
sys.path.insert(0, str(PIPELINES_DIR))
load_dotenv(PIPELINES_DIR / ".env")

# Import helper functions
from utils.cloud_helpers import load_table_to_bigquery

BUCKET_URL = os.getenv("BUCKET_URL")
BIGQUERY_PATH = os.getenv("WAREHOUSE_SCHEMA")


# Retrieve cleaned product tables
def load_product_tables(logger):
    product_tables = ["features", "labels", "products", "related_products", "sizes"]
    for table in product_tables:
        gcs_url = f"{BUCKET_URL}/api-pipeline/clean/{table}.csv"
        table_id = f"{BIGQUERY_PATH}.{table}"
        load_table_to_bigquery(gcs_url, table_id)
        logger.info(f"{table.title()} successfully loaded to warehouse")


# Retrieve cleaned order tables
def load_order_tables(logger):
    order_tables = ["orders", "order_details"]
    for table in order_tables:
        gcs_url = f"{BUCKET_URL}/api-pipeline/clean/{table}.csv"
        table_id = f"{BIGQUERY_PATH}.{table}"
        load_table_to_bigquery(gcs_url, table_id)
        logger.info(f"{table.title()} successfully loaded to warehouse")


def load_data(new_products, new_orders, logger):
    t1 = time.perf_counter()
    logger.info("LOADING DATA STARTED...")

    # Load data to warehouse if there are new records
    if new_products:
        load_product_tables(logger)
    else:
        logger.info("No new products data")

    if new_orders:
        load_order_tables(logger)
    else:
        logger.info("No new orders data")

    # Log execution time
    t2 = time.perf_counter()
    logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
    logger.info("----------------------------------------------------------------")
