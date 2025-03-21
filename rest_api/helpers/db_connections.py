from dotenv import load_dotenv
from sqlalchemy import create_engine
from pymongo import MongoClient
import os

load_dotenv(".credentials")

# postgres connection
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = "postgres-db"
PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
SCHEMA = os.getenv("POSTGRES_SCHEMA")
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?options=-csearch_path%3D{SCHEMA}")

# mongo connection
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
mongo_db = client[os.getenv("MONGO_DB")]
mongo_collection = mongo_db["product_features"]
