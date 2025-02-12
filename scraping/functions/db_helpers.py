from sqlalchemy import create_engine, text
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import os

load_dotenv(".credentials")

# POSTGRES
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
SCHEMA = os.getenv("POSTGRES_SCHEMA")

engine = create_engine(
    f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?options=-csearch_path%3D{SCHEMA}"
)

# MONGO
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
mongo_db = client["football-project"]
mongo_product_features = mongo_db["product_features"]


def get_scraped_ids():
    with engine.connect() as conn:
        boots_ids = conn.execute(
            text("SELECT scraped_id FROM products WHERE category_id = 1")
        ).fetchall()
        balls_ids = conn.execute(
            text("SELECT scraped_id FROM products WHERE category_id = 2")
        ).fetchall()

    boots, balls = set([int(row[0]) for row in boots_ids]), set(
        [int(row[0]) for row in balls_ids]
    )
    return boots, balls


def get_max_product_id():
    with engine.connect() as conn:
        max_product_id = conn.execute(
            text("SELECT COALESCE(MAX(product_id), 0) FROM products")
        ).scalar()
    return max_product_id


def load_to_db(table_name, clean_data_path, file_name):
    df = pd.read_csv(clean_data_path / file_name, sep=";")
    df.to_sql(table_name, engine, if_exists="append", index=False)


def update_summary_table():
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM products")).scalar()
        last_total = conn.execute(
            text(
                "SELECT COALESCE(total, 0) FROM summary ORDER BY created_at DESC LIMIT 1"
            )
        ).scalar()
        new = last_total - total if last_total else 0

        row = {"created_at": datetime.now(), "total": total, "new": new}
        query = text(
            "INSERT INTO summary (created_at, total, new) VALUES (:created_at, :total, :new)"
        )
        conn.execute(query, row)
        conn.commit()
