import pandas as pd
from pathlib import Path
import json
import sys

# Set base path for helper functions and paths
base_path = Path.cwd() / "scraping"
sys.path.append(str(base_path))
from functions.logs import logs_setup
from functions.db_helpers import (
    load_to_db,
    update_summary_table,
    mongo_product_features,
)

# Define paths
data_dir = base_path / "data"
clean_data_path = data_dir / "cleaned"

# Setup logging
logger = logs_setup("load_data.log")


# Load data to postgres db and update summary table
try:
    load_to_db("products", clean_data_path, "products.csv")
    load_to_db("sizes", clean_data_path, "sizes.csv")
    load_to_db("colors", clean_data_path, "colors.csv")
    load_to_db("labels", clean_data_path, "labels.csv")
    logger.info("Data successfully loaded to postgres db")

    # Update summary table
    update_summary_table()
    logger.info("Summary table successfully updated")

except Exception:
    logger.error("Unexpected error", exc_info=True)


# Load data to mongo db
try:
    # open cleaned json file
    with open(clean_data_path / "product_features.json", "r") as f:
        product_features = json.load(f)

    features_lst = [
        {"_id": key, **value}
        for key, value in product_features.items()
        if type(value) == dict
    ]
    mongo_product_features.insert_many(features_lst)
    logger.info("Data successfully loaded to mongo db")

except Exception:
    logger.error("Unexpected error", exc_info=True)


logger.info("----------")
