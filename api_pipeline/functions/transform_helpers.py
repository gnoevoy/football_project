import pandas as pd
import numpy as np

from functions.gcs_utils import get_file_from_bucket


def load_products():
    products = pd.DataFrame()
    categories = ["boots", "balls"]

    for index, category in enumerate(categories, start=1):
        data = get_file_from_bucket("api-pipeline/raw", f"{category}.json", "json")
        df = pd.DataFrame(data["products"])
        df["category_name"] = data["info"]["category_name"]
        df["category_id"] = index
        products = pd.concat([products, df], ignore_index=True)

    return products


# need to check after loaidng if everythig is correct (cleaning steps)


def get_products_and_sizes(df):
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["description"] = df["description"].apply(lambda value: value if value else np.nan)
    df["product_color"] = np.where(df["product_color"].str.split().str.len() <= 2, df["product_color"], np.nan)

    # is it possbile to do faster with parrallelization???
    lst = []
    for _, row in df[["product_id", "sizes"]].iterrows():
        if row["sizes"]:
            for size in row["sizes"]:
                lst.append({"product_id": row["product_id"], **size})

    data = df.drop(columns=["sizes"])
    return data, pd.DataFrame(lst)


def get_orders_and_details():
    data = get_file_from_bucket("api-pipeline/raw", "orders.json", "json")
    orders = pd.DataFrame(data)

    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["created_at"] = pd.to_datetime(orders["created_at"])

    # is it possbile to do faster with parrallelization???
    lst = []
    for _, row in orders[["order_id", "order_details"]].iterrows():
        if row["order_details"]:
            for detail in row["order_details"]:
                lst.append({"order_id": row["order_id"], **detail})

    return orders.drop(columns=["order_details"]), pd.DataFrame(lst)
