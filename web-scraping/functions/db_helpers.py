from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pymongo import MongoClient
from google.cloud import storage
from google.cloud.storage import transfer_manager
from datetime import datetime, timezone
import os

load_dotenv(".credentials")


def example():
    return 1


# CONNECTIONS

# postgres connection
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
SCHEMA = os.getenv("POSTGRES_SCHEMA")

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?options=-csearch_path%3D{SCHEMA}")


# mongo connection
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
mongo_db = client[os.getenv("MONGO_DB")]
mongo_collection = mongo_db["product_features"]


# gcp connection
bucket_name = os.getenv("BUCKET_NAME")


# HELPER FUNCTIONS


# Get lists with existed products from db
def get_scraped_ids():
    with engine.connect() as conn:
        boots_ids = conn.execute(text("SELECT scraped_id FROM products WHERE category_id = 1")).fetchall()
        balls_ids = conn.execute(text("SELECT scraped_id FROM products WHERE category_id = 2")).fetchall()
        boots = set([int(row[0]) for row in boots_ids])
        balls = set([int(row[0]) for row in balls_ids])
    return boots, balls


# Get the highest product id from db
def get_max_product_id():
    with engine.connect() as conn:
        max_product_id = conn.execute(text("SELECT COALESCE(MAX(product_id), 0) FROM products")).scalar()
    return int(max_product_id)


# Load dataframe to db
def load_to_db(df, table_name):
    df.to_sql(table_name, engine, if_exists="append", index=False)


# Update summary table, track how many records were added from scraping
def update_summary_table():
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM products")).scalar()
        last_total = conn.execute(text("SELECT COALESCE(total, 0) FROM summary ORDER BY created_at DESC LIMIT 1")).scalar()
        new = last_total - total if last_total else 0
        row = {"created_at": datetime.now(timezone.utc), "total": total, "new": new}

        # Insert record and commit changes
        query = text("INSERT INTO summary (created_at, total, new) VALUES (:created_at, :total, :new)")
        conn.execute(query, row)
        conn.commit()
    return new


# Load list of dictionaries to mongo
def load_to_mongo(lst):
    mongo_collection.insert_many(lst)
    return len(lst)


# Extract all images and load to storage with prefix
def upload_images_to_storage(img_dir, workers=8):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    string_paths = [str(path.relative_to(img_dir)) for path in img_dir.rglob("*") if path.is_file()]

    results = transfer_manager.upload_many_from_filenames(
        bucket=bucket,
        filenames=string_paths,
        source_directory=img_dir,
        blob_name_prefix="product-images/",
        max_workers=workers,
    )

    return len(string_paths)
