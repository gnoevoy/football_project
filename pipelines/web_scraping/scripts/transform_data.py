from pathlib import Path
import numpy as np
import time
import sys

# Add python path
PIPELINES_DIR = Path(__file__).parents[2]
sys.path.insert(0, str(PIPELINES_DIR))

# Import helper functions
from utils.cloud_helpers import get_file_from_bucket, load_file_to_bucket


# Get raw files from the bucket
def get_files(logger):
    files_dir = "web-scraping/raw"
    products = get_file_from_bucket(files_dir, "products", file_type="csv")
    sizes = get_file_from_bucket(files_dir, "sizes", file_type="csv")
    details = get_file_from_bucket(files_dir, "details.json", file_type="json")
    logger.info("Files were successfully downloaded from the bucket.")
    return products, sizes, details


# Clean and transform the products DataFrame
def transform_products(products):
    products["price"] = products["price"].str.split("\n", expand=True)[1].str.strip().str[:-2].str.replace(",", ".").astype(float)
    products["title"] = products["title"].str.split("\n", expand=True)[0].str.strip().str.title()
    products["avg_vote_rate"] = np.where(products["avg_vote_rate"] == 0, np.nan, products["avg_vote_rate"])
    products["num_votes"] = np.where(products["num_votes"] == 0, np.nan, products["num_votes"])
    if products["old_price"].dtype == "object":
        products["old_price"] = products["old_price"].str.split("\n", expand=True)[1].str.strip().str[:-2].str.replace(",", ".").astype(float)

    return products


# Process sizes
def transform_sizes(sizes):
    sizes["size"] = sizes["size"].astype("str").str.strip()
    return sizes


# Process details JSON data and convert to list
def transform_details(dct):
    details = []

    for product in dct:
        product_id = int(product["product_id"])
        labels = [label.strip().title() for label in product["labels"]]
        related_products = [int(item.strip()) for item in product["related_products"]]

        features = {}
        for key, value in product["features"].items():
            # Standardize feature keys and clean their values
            if key == "Class:":
                new_key = "type_of_class"
            else:
                new_key = key.strip().lower().replace(" ", "_").replace(":", "").replace("'", "")
            new_value = value.strip().title()
            features[new_key] = new_value

        product_details = {"_id": product_id, "product_id": product_id, "labels": labels, "related_products": related_products, "features": features}
        details.append(product_details)

    return details


def load_files(products, sizes, details, logger):
    destination = "web-scraping/clean"
    load_file_to_bucket(products, destination, "products", file_type="csv")
    load_file_to_bucket(sizes, destination, "sizes", file_type="csv")
    load_file_to_bucket(details, destination, "details.json", file_type="json")
    logger.info("Files were successfully uploaded to bucket")


def transform_data(logger):
    try:
        logger.info("DATA TRANSFORMATION STARTED ...")
        t1 = time.perf_counter()

        # Get files from bucket, transform them and load storage
        products, sizes, details = get_files(logger)
        products_df = transform_products(products)
        sizes_df = transform_sizes(sizes)
        details_dct = transform_details(details)
        logger.info("Data transformation was successful")
        load_files(products_df, sizes_df, details_dct, logger)

        # Log execution time
        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
    except:
        logger.error(f"", exc_info=True)
