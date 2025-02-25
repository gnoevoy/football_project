from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pymongo import MongoClient
from google.cloud import storage
import os

load_dotenv(".credentials")

# postgres connection
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
SCHEMA = os.getenv("POSTGRES_SCHEMA")

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?options=-csearch_path%3D{SCHEMA}")


# mongo connection
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
mongo_db = client[os.getenv("MONGO_DB")]
mongo_collection = mongo_db["product_features"]


# gcs connection
bucket_name = os.getenv("BUCKET_NAME")
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)


def postgres_check_connection():
    with engine.connect() as conn:
        response = conn.execute(text("SELECT 1"))
    return True if response else False


def mongo_check_connection():
    response = mongo_db.command("ping")
    return response.get("ok") == 1.0


def gcs_check_connection():
    response = bucket.exists()
    return True if response else False
