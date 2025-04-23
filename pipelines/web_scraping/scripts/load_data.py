from pathlib import Path
import time
import sys

# Add python path
PIPELINES_DIR = Path(__file__).parents[2]
sys.path.insert(0, str(PIPELINES_DIR))

# Import helper functions
from web_scraping.functions.db_helpers import load_to_postgre, load_to_mongo, update_summary_table
from utils.cloud_helpers import get_file_from_bucket


# Get cleaned files from the bucket
def get_files(logger):
    files_dir = "web-scraping/clean"
    products = get_file_from_bucket(files_dir, "products", file_type="csv")
    sizes = get_file_from_bucket(files_dir, "sizes", file_type="csv")
    details = get_file_from_bucket(files_dir, "details.json", file_type="json")
    logger.info("Files were successfully downloaded from the bucket.")
    return products, sizes, details


def load_data_to_db(products, sizes, details, logger):
    # Load products and sizes data into PostgreSQL
    load_to_postgre(products, "products")
    load_to_postgre(sizes, "sizes")

    # Load product details into MongoDB
    products_num = len(products)
    mongo_num = load_to_mongo(details)
    logger.info(f"Data was successfully loaded, postgres: {products_num}, mongo: {mongo_num}")

    # Calculate values for summary table record
    boots = len(products.query("category_id == 1"))
    balls = len(products.query("category_id == 2"))
    return boots, balls


def load_data(logger):
    logger.info("LOADING DATA STARTED ...")
    t1 = time.perf_counter()

    # Load data to db's and update summary table
    products, sizes, details = get_files(logger)
    boots, balls = load_data_to_db(products, sizes, details, logger)
    update_summary_table(boots, balls)
    logger.info(f"Summary table successfully updated, boots: {boots}, balls {balls}")

    # Log execution time
    t2 = time.perf_counter()
    logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
    logger.info("----------------------------------------------------------------")
