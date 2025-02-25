from pathlib import Path
import sys

# Set base path for helper functions
WEB_SCRAPING_DIR = Path(__file__).parent.parent
sys.path.append(str(WEB_SCRAPING_DIR))

# Import helper functions
from functions.clean_data_helpers import clean_csv_files, clean_json_file, get_min_id_by_category
from functions.db_helpers import load_to_db, update_summary_table, load_to_mongo
from functions.bucket_helpers import open_file_from_gcs, move_image_to_gcs


def clean_and_load_data(logger):

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
        boots_id, balls_id = get_min_id_by_category(products)
        logger.info("Data successfully cleaned")

        logger.info("")
        logger.info("LOADING STARTED")

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
        images_num = move_image_to_gcs()
        logger.info(f"Images successfully loaded to storage, added {images_num} new images")
        logger.info("")

    except Exception:
        logger.error(f"Unexpected error", exc_info=True)
        logger.info("")


if __name__ == "__main__":
    clean_and_load_data()
