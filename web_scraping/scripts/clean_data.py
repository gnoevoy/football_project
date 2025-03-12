from pathlib import Path
import sys

# Set base path for helper functions
WEB_SCRAPING_DIR = Path(__file__).parent.parent
sys.path.append(str(WEB_SCRAPING_DIR))

# Import helper functions
from functions.clean_data_helpers import clean_csv_files, clean_json_file, get_min_id_by_category
from functions.db_helpers import load_to_db, update_summary_table, load_to_mongo
from functions.bucket_helpers import open_file_from_gcs, move_image_to_gcs, delete_blobs_from_gcs


def clean_data(logger):

    try:
        logger.info("DATA PREPARATION STARTED")

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
        boots_num, balls_num = get_min_id_by_category(products)
        logger.info("Data successfully cleaned")

        logger.info("")

    except Exception:
        logger.error(f"Unexpected error", exc_info=True)
        logger.info("")


if __name__ == "__main__":
    clean_data()
