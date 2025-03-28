from pathlib import Path
import sys


ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

from functions.transform_helpers import load_products, get_products_and_sizes, get_orders_and_details
from functions.gcs_utils import load_file_to_bucket

# import files


def transform_data():
    raw_products = load_products()
    products, sizes = get_products_and_sizes(raw_products)
    orders, order_details = get_orders_and_details()

    print(order_details.columns)
    print(order_details.head(3))

    # load_file_to_bucket(products, "api-pipeline/clean", "products", "csv")
    # load_file_to_bucket(sizes, "api-pipeline/clean", "sizes", "csv")
    # load_file_to_bucket(orders, "api-pipeline/clean", "orders", "csv")
    # load_file_to_bucket(order_details, "api-pipeline/clean", "order_details", "csv")


transform_data()
