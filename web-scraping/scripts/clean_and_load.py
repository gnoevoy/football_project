import pandas as pd
from pathlib import Path
import traceback
import json
import sys

# Set base path for helper functions and paths
base_path = Path.cwd() / "web-scraping"
sys.path.append(str(base_path))

# Import helper functions
from functions.logger import logs_setup
from functions.clean_data_helpers import clean_csv_files, clean_json_file
from functions.db_helpers import load_to_db, update_summary_table, load_to_mongo, upload_images_to_storage

# Setup logging
logger = logs_setup("clean_and_load.log")

# Define paths
data_dir = base_path / "data"
img_dir = data_dir / "img"
raw_data_path = data_dir / "raw"


try:
    logger.info("DATA PREPARATION STARTED ...")

    # Import files
    products = pd.read_csv(raw_data_path / "products.csv", delimiter=";", parse_dates=["created_at"])
    colors = pd.read_csv(raw_data_path / "colors.csv", delimiter=";")
    sizes = pd.read_csv(raw_data_path / "sizes.csv", delimiter=";")
    labels = pd.read_csv(raw_data_path / "labels.csv", delimiter=";")
    images = pd.read_csv(raw_data_path / "images.csv", delimiter=";")

    with open(raw_data_path / "product_features.json", "r") as f:
        features = json.load(f)

    logger.info("Data successfully imported")

    # Data cleaning and transformations
    clean_csv_files(products, labels, sizes)
    product_features = clean_json_file(features)
    logger.info("Data successfully cleaned")

    logger.info("")
    logger.info("LOADING STARTED ...")

    # Load to postgres db
    load_to_db(products, "products")
    load_to_db(colors, "colors")
    load_to_db(sizes, "sizes")
    load_to_db(labels, "labels")
    load_to_db(images, "images")
    logger.info("Data successfully loaded to db")

    # Update summary table
    summary_num = update_summary_table()
    logger.info(f"Summary table successfully updated, added {summary_num} new products")

    # Load product features to mongo
    mongo_num = load_to_mongo(product_features)
    logger.info(f"Data successfully loaded to mongo, added {mongo_num} records")

    # Load images to storage
    images_num = upload_images_to_storage(img_dir)
    logger.info(f"Images successfully loaded to storage, added {images_num} new images")

except Exception:
    logger.error(f"Unexpected error", exc_info=True)
    traceback.print_exc()

logger.info("")
logger.info("--------------------------------------------------------------------")
logger.info("")
