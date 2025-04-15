import pandas as pd
import numpy as np
from pathlib import Path
import sys


# add path path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# import helper functions
from functions.gcs_utils import get_file_from_bucket


# featch category table
def get_category_table(raw_files_dir, category):
    data = get_file_from_bucket(raw_files_dir, f"{category}.json", "json")
    df = pd.DataFrame(data["products"])
    df["category_name"] = data["category_name"]
    return df


def get_products_with_details():
    categories = ["boots", "balls"]
    products = pd.DataFrame()

    # construct one table from multiple categories
    for category in categories:
        df = get_category_table("api-pipeline/raw", category)
        df["category_id"] = np.where(category == "boots", 1, 2)
        products = pd.concat([products, df], ignore_index=True)
    return products


x = get_products_with_details()
x.to_csv("example_data.csv", index=False)
