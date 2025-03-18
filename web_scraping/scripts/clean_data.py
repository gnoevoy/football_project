from pathlib import Path
import sys

# Set base path for helper functions
WEB_SCRAPING_DIR = Path(__file__).parent.parent
sys.path.append(str(WEB_SCRAPING_DIR))

# Import helper functions
from functions.clean_data_helpers import clean_csv_files, clean_json_file
from functions.bucket_helpers import open_file_from_gcs, load_file_to_gcs


def clean_data(logger):
    raw_files_dir = "web-scraping/raw"
    clean_files_dir = "web-scraping/clean"

    try:
        logger.info("DATA CLEANING STARTED")

        # Import files
        products = open_file_from_gcs(raw_files_dir, "products.csv")
        colors = open_file_from_gcs(raw_files_dir, "colors.csv")
        sizes = open_file_from_gcs(raw_files_dir, "sizes.csv")
        labels = open_file_from_gcs(raw_files_dir, "labels.csv")
        images = open_file_from_gcs(raw_files_dir, "images.csv")
        features = open_file_from_gcs(raw_files_dir, "features.json", csv=False)

        logger.info("Data successfully imported")

        # Data cleaning and transformations
        clean_csv_files(products, labels, sizes)
        product_features = clean_json_file(features)
        logger.info("Data successfully cleaned")

        # Export data to bucket
        load_file_to_gcs(products, clean_files_dir, "products.csv")
        load_file_to_gcs(labels, clean_files_dir, "labels.csv")
        load_file_to_gcs(colors, clean_files_dir, "colors.csv")
        load_file_to_gcs(sizes, clean_files_dir, "sizes.csv")
        load_file_to_gcs(images, clean_files_dir, "images.csv")
        load_file_to_gcs(product_features, clean_files_dir, "features.json", csv=False)

        logger.info("Cleaned data successfully loaded to bucket")
        logger.info("")

    except Exception:
        logger.error(f"Unexpected error", exc_info=True)
        logger.info("")


if __name__ == "__main__":
    clean_data()
