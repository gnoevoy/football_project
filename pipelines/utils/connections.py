from google.cloud import bigquery
from sqlalchemy import create_engine
from pymongo import MongoClient
from google.cloud import storage
from dotenv import load_dotenv
from pathlib import Path
import os

# Import environment variables
ROOT_DIR = Path(__file__).parents[1]
if ROOT_DIR.exists():
    load_dotenv(ROOT_DIR / ".env")

# Postgres connection
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
SCHEMA = os.getenv("POSTGRES_SCHEMA")
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?options=-csearch_path%3D{SCHEMA}")

# Mongo connection
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
mongo_db = client[os.getenv("MONGO_DB")]
mongo_collection = mongo_db["product_details"]

# Cloud connections
bucket_name = os.getenv("BUCKET_NAME")
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
bigquery_client = bigquery.Client()
