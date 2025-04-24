from dotenv import load_dotenv
from pathlib import Path
import sys
import os

# Add python path and load variables
PIPELINES_DIR = Path(__file__).parents[2]
sys.path.insert(0, str(PIPELINES_DIR))
ENV_FILE = PIPELINES_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

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

    logger.info("----------------------------------------------------------------")
