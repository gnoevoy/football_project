from pathlib import Path
import traceback
import sys

# Set base path for helper functions and paths
base_path = Path.cwd() / "web-scraping"
sys.path.append(str(base_path))

# Import helper functions
from functions.logger import logs_setup
from functions.clean_data_helpers import clean_csv_files, clean_json_file, get_min_id_by_category
from functions.db_helpers import load_to_db, update_summary_table, load_to_mongo
from functions.bucket_helpers import open_file_from_gcs, move_image_in_gcs

# Setup logging
logger = logs_setup("clean_and_load.log")


try:
    logger.info("")
    logger.info("DATA PREPARATION STARTED ...")

    # Import files
    products = open_file_from_gcs("products.csv")
    colors = open_file_from_gcs("colors.csv")
    sizes = open_file_from_gcs("sizes.csv")
    labels = open_file_from_gcs("labels.csv")
    images = open_file_from_gcs("images.csv")
    features = open_file_from_gcs("product_features.json", csv=False)

    logger.info("Data successfully imported")

    # Data cleaning and transformations
    clean_csv_files(products, labels, sizes)
    product_features = clean_json_file(features)
    boots_id, balls_id = get_min_id_by_category(products)
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
    summary_num = update_summary_table(boots_id, balls_id)
    logger.info(f"Summary table successfully updated, added {summary_num} new products")

    # Load product features to mongo
    mongo_num = load_to_mongo(product_features)
    logger.info(f"Data successfully loaded to mongo, added {mongo_num} records")

    # Load images to storage
    images_num = move_image_in_gcs()
    logger.info(f"Images successfully loaded to storage, added {images_num} new images")

except Exception:
    logger.error(f"Unexpected error", exc_info=True)
    traceback.print_exc()

logger.info("")
logger.info("--------------------------------------------------------------------")
