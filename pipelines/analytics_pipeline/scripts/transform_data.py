from pathlib import Path
import sys

# Add path path
PIPELINES_DIR = Path(__file__).parents[2]
sys.path.insert(0, str(PIPELINES_DIR))

# Import helper functions
from utils.cloud_helpers import load_file_to_bucket
from analytics_pipeline.scripts.transform_helpers import (
    get_products_and_orders_ids,
    get_products_with_details,
    get_products,
    get_labels,
    get_related_products,
    get_sizes,
    get_features,
    get_orders_and_details,
)


# Wrapper function to handle products data logic
def products_wrapper(products_ids, clean_files_dir, logger):
    # Get single dataframe with all products data
    df = get_products_with_details(products_ids)
    logger.info("Produts data successfully extracted")

    # Check if there are new records, if so load to bucket
    if len(df) > 0:
        products = get_products(df)
        labels = get_labels(df)
        related_products = get_related_products(df)
        sizes = get_sizes(df)
        features = get_features(df)

        # Load dataframes to bucket + logs
        load_file_to_bucket(products, clean_files_dir, "products.csv", "csv")
        load_file_to_bucket(labels, clean_files_dir, "labels.csv", "csv")
        load_file_to_bucket(related_products, clean_files_dir, "related_products.csv", "csv")
        load_file_to_bucket(sizes, clean_files_dir, "sizes.csv", "csv")
        load_file_to_bucket(features, clean_files_dir, "features.csv", "csv")
        logger.info(
            f"Data successfully loaded to bucket, products: {len(products)}, labels: {len(labels)}, related_products: {len(related_products)}, sizes: {len(sizes)}, features: {len(features)}"
        )

        # Important boolean to determine if there are new records, helps in the next script (load_data.py)
        new_records = True
        return new_records
    else:
        logger.info("Products data didnt loaded to bucket due to no new records")
        new_records = False
        return new_records


# Wrapper function to handle orders data logic
def orders_wrapper(order_ids, clean_files_dir, logger):
    orders, order_details = get_orders_and_details(order_ids)
    logger.info("Orders data successfully extracted")

    # Check if there are new records, if so load to bucket
    if len(orders) > 0:
        load_file_to_bucket(orders, clean_files_dir, "orders.csv", "csv")
        load_file_to_bucket(order_details, clean_files_dir, "order_details.csv", "csv")
        logger.info(f"Data successfully loaded to bucket, orders: {len(orders)}, order_details: {len(order_details)}")

        # The same boolean as in the products wrapper
        new_records = True
        return new_records
    else:
        logger.info("Orders data didn't loaded to bucket due to no new records")
        new_records = False
        return new_records


def transform_data(logger):
    logger.info("DATA TRANSFORMATION STARTED ...")
    clean_files_dir = "api-pipeline/clean"

    # Get ids to prevent loading duplicate records to bigquery
    product_ids, order_ids = get_products_and_orders_ids()
    # Retrieve data, transform it and if there are new records load to bucket
    new_products = products_wrapper(product_ids, clean_files_dir, logger)
    new_orders = orders_wrapper(order_ids, clean_files_dir, logger)

    logger.info("----------------------------------------------------------------")
    return new_products, new_orders
