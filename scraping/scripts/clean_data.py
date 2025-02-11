import pandas as pd
import numpy as np
from pathlib import Path
import json
import sys

# Set base path for helper functions and paths
base_path = Path.cwd() / "scraping"
sys.path.append(str(base_path))
from functions.logs import logs_setup

# Define paths
data_dir = base_path / "data"
raw_data_path = data_dir / "raw"
clean_data_path = data_dir / "cleaned"


# Setup logging
logger = logs_setup("clean_data.log")

try:
    # Import files
    products = pd.read_csv(
        raw_data_path / "products.csv", delimiter=";", parse_dates=["created_at"]
    )
    colors = pd.read_csv(raw_data_path / "colors.csv", delimiter=";")
    sizes = pd.read_csv(raw_data_path / "sizes.csv", delimiter=";")
    labels = pd.read_csv(raw_data_path / "labels.csv", delimiter=";")

    with open(raw_data_path / "product_features.json", "r") as f:
        features = json.load(f)

    logger.info("Data successfully imported")

    # Data cleaning and transformations

    # Products table
    products["price"] = (
        products["price"]
        .str.split("\n", expand=True)[1]
        .str.strip()
        .str[:-2]
        .str.replace(",", ".")
        .astype(float)
    )
    products["old_price"] = (
        products["old_price"]
        .str.split("\n", expand=True)[1]
        .str.strip()
        .str[:-2]
        .str.replace(",", ".")
        .astype(float)
    )
    products["title"] = (
        products["title"].str.split("\n", expand=True)[0].str.strip().str.title()
    )

    # Others tables
    labels["label"] = labels["label"].str.strip().str.title()
    sizes["in_stock"] = np.where(sizes["in_stock"] == 1, True, False)

    # Json file
    product_features = {}
    for product_id, features in features.items():
        if type(features) == dict:
            values = {}
            for param, value in features.items():
                title = param[:-1].strip().title()
                text = value.strip().title()
                values[title] = text
            product_features[product_id] = values
        else:
            product_features[product_id] = features

    logger.info("Data successfully cleaned")

except Exception:
    logger.error("Can't import and clean data", exc_info=True)


try:
    # helper functions to export CSV files
    def export_to_csv(data, clean_data_path, file_name):
        df = pd.DataFrame(data)
        df.to_csv(clean_data_path / file_name, index=False, sep=";")

    export_to_csv(products, clean_data_path, "products.csv")
    export_to_csv(colors, clean_data_path, "colors.csv")
    export_to_csv(sizes, clean_data_path, "sizes.csv")
    export_to_csv(labels, clean_data_path, "labels.csv")

    with open(clean_data_path / "product_features.json", "w") as f:
        json.dump(product_features, f, indent=4)

    logger.info("Files were successfully written")

except Exception:
    logger.error("Can't export data", exc_info=True)
logger.info("----------")
