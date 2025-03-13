from pathlib import Path
import sys

# Set base path for helper functions
WEB_SCRAPING_DIR = Path(__file__).parent.parent
sys.path.append(str(WEB_SCRAPING_DIR))

# Import helper functions
from functions.clean_data_helpers import clean_csv_files, clean_json_file
from functions.bucket_helpers import open_file_from_gcs, move_image_gcs
from functions.db_helpers import load_to_db, update_summary_table, load_to_mongo


def clean_and_load_data(logger):

    try:
        logger.info("DATA CLEANING STARTED")

        # Import files
        raw_files_dir = "web-scraping/raw"
        products = open_file_from_gcs(raw_files_dir, "products.csv")
        colors = open_file_from_gcs(raw_files_dir, "colors.csv")
        sizes = open_file_from_gcs(raw_files_dir, "sizes.csv")
        labels = open_file_from_gcs(raw_files_dir, "labels.csv")
        images = open_file_from_gcs(raw_files_dir, "images.csv")
        features = open_file_from_gcs(raw_files_dir, "product_features.json", csv=False)

        logger.info("Data successfully imported")

        # Data cleaning and transformations
        clean_csv_files(products, labels, sizes)
        product_features = clean_json_file(features)
        logger.info("Data successfully cleaned")
        logger.info("")

        logger.info("DATA LOADING STARTED")

        # Load to postgres db
        load_to_db(products, "products")
        if len(colors) > 0:
            load_to_db(colors, "colors")
        if len(labels) > 0:
            load_to_db(labels, "labels")
        load_to_db(sizes, "sizes")
        load_to_db(images, "images")
        logger.info("Data successfully loaded to db")

        # Update summary table
        boots_num = len(products.query("category_id == 1"))
        balls_num = len(products.query("category_id == 2"))
        summary_num = update_summary_table(boots_num, balls_num)
        logger.info(f"Summary table successfully updated, added {summary_num} new products")

        # Load product features to mongo
        mongo_num = load_to_mongo(product_features)
        logger.info(f"Data successfully loaded to mongo, added {mongo_num} records")

        # Load images to storage
        images_num = move_image_gcs()
        logger.info(f"Images successfully moved, {images_num} images")
        logger.info("")

    except Exception:
        logger.error(f"Unexpected error", exc_info=True)
        logger.info("")


if __name__ == "__main__":
    clean_and_load_data()
