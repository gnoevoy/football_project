from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import numpy as np
import sys
import os

# Add python path and load variables
PIPELINES_DIR = Path(__file__).parents[2]
sys.path.insert(0, str(PIPELINES_DIR))
load_dotenv(PIPELINES_DIR / ".env")

# Import helper functions
from utils.cloud_helpers import get_file_from_bucket, bigquery_client


# Retrieve product and order IDs from BigQuery
def get_products_and_orders_ids():
    BIGQUERY_SCHEMA = os.getenv("WAREHOUSE_SCHEMA")
    products_query = bigquery_client.query(f"SELECT product_id FROM {BIGQUERY_SCHEMA}.products").result()
    orders_query = bigquery_client.query(f"SELECT order_id FROM {BIGQUERY_SCHEMA}.orders").result()
    products = [product.product_id for product in products_query]
    orders = [order.order_id for order in orders_query]
    return products, orders


# Get products data in one dataframe
def get_products_with_details(product_ids):
    df = pd.DataFrame()

    for category in ["boots", "balls"]:
        data = get_file_from_bucket("api-pipeline/raw", f"{category}.json", "json")
        category_id = 1 if category == "boots" else 2
        category_df = pd.json_normalize(data["products"], errors="ignore")
        category_df["category_name"] = data["category_name"]
        category_df["category_id"] = category_id
        df = pd.concat([df, category_df], ignore_index=True)

    # filter out table to get only new products
    df = df[~df["product_id"].isin(product_ids)]
    return df


### Normalize products data (create star schema, 5 tables)


def get_products(df):
    cols = ["product_id", "created_at", "title", "price", "old_price", "description", "avg_vote_rate", "num_votes", "category_id"]
    products = df[cols]
    products["description"] = products["description"].replace({None: np.nan})
    products["num_votes"] = products["num_votes"].astype("Int64")
    return products


def get_labels(df):
    labels = df[["product_id", "labels"]].explode("labels").dropna().rename(columns={"labels": "label"})
    labels["label"] = labels["label"].astype(str)
    return labels


def get_related_products(df):
    related_products = df[["product_id", "related_products"]].explode("related_products").dropna()
    related_products.rename(columns={"related_products": "related_product_id"}, inplace=True)
    related_products["related_product_id"] = related_products["related_product_id"].astype(int)
    return related_products


def get_sizes(df):
    sizes = pd.DataFrame()
    for col in ["sizes.in_stock", "sizes.out_of_stock"]:
        exploded = df[["product_id", col]].explode(col).dropna().rename(columns={col: "size"})
        exploded["in_stock"] = True if col == "sizes.in_stock" else False
        sizes = pd.concat([sizes, exploded], ignore_index=True)
    sizes["size"] = sizes["size"].astype(str)
    return sizes


def get_features(df):
    cols = [col for col in df.columns if "features." in col]
    features = df[["product_id", *cols]]
    features = features.melt(id_vars=["product_id"], value_vars=cols, var_name="feature", value_name="value").dropna()
    features["feature"] = features["feature"].str.split(".").str[1]
    return features


# Return orders and order details tables
def get_orders_and_details(order_ids):
    data = get_file_from_bucket("api-pipeline/raw", "orders.json", "json")
    orders_lst, details_lst = [], []

    for order in data:
        # Filter out orders to get only new orders
        if order["order_id"] not in order_ids:
            order_id = order["order_id"]
            details = [{"order_id": order_id, **detail} for detail in order["order_details"]]
            details_lst.extend(details)
            row = {**order}
            row.pop("order_details")
            orders_lst.append(row)

    return pd.DataFrame(orders_lst), pd.DataFrame(details_lst)
