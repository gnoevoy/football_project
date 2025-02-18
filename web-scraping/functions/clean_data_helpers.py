import pandas as pd
import numpy as np


def clean_csv_files(products, labels, sizes):
    # clean product table
    products["price"] = products["price"].str.split("\n", expand=True)[1].str.strip().str[:-2].str.replace(",", ".").astype(float)
    products["old_price"] = products["old_price"].str.split("\n", expand=True)[1].str.strip().str[:-2].str.replace(",", ".").astype(float)
    products["title"] = products["title"].str.split("\n", expand=True)[0].str.strip().str.title()
    products["avg_vote_rate"] = np.where(products["avg_vote_rate"] == 0, np.nan, products["avg_vote_rate"])
    products["num_votes"] = np.where(products["num_votes"] == 0, np.nan, products["num_votes"])

    # additional tables
    labels["label"] = labels["label"].str.strip().str.title()
    sizes["size"] = sizes["size"].astype("str").str.strip()


def get_min_id_by_category(products):
    balls = products.query("category_id == 2")["product_id"].min()
    boots = products.query("category_id == 1")["product_id"].min()
    return boots, balls


def clean_json_file(file_name):
    product_features = []

    # Unpack dictionary, clean records and append to a list
    for id, features in file_name.items():
        row = {"_id": id, "product_id": id}

        for feature, value in features.items():
            key = feature.strip().lower().replace(" ", "_").replace(":", "").replace("'", "")
            data = value.strip().title()
            row[key] = data
        product_features.append(row)

    return product_features
