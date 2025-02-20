from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pymongo import MongoClient
from datetime import datetime, timezone
import os

load_dotenv(".credentials")

# CONNECTIONS

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
def update_summary_table(boots_id, balls_id):
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM products")).scalar()

        if boots_id:
            new_boots = conn.execute(text(f"SELECT COUNT(*) FROM products WHERE category_id = 1 AND product_id >= {boots_id}")).scalar()
        else:
            new_boots = 0

        if balls_id:
            new_balls = conn.execute(text(f"SELECT COUNT(*) FROM products WHERE category_id = 2 AND product_id >= {balls_id}")).scalar()
        else:
            new_balls = 0

        row = {
            "created_at": datetime.now(timezone.utc),
            "total": total if total else 0,
            "new_boots": new_boots if new_boots else 0,
            "new_balls": new_balls if new_balls else 0,
        }

        # Insert record and commit changes
        query = text("INSERT INTO summary (created_at, total, new_boots, new_balls) VALUES (:created_at, :total, :new_boots, :new_balls)")
        conn.execute(query, row)
        conn.commit()
    return new_balls + new_boots


# Load list of dictionaries to mongo
def load_to_mongo(lst):
    mongo_collection.insert_many(lst)
    return len(lst)


# Get the highest order id from db
def order_generetor_queries():
    with engine.connect() as conn:
        max_order_id = conn.execute(text("SELECT COALESCE(MAX(order_id), 0) FROM orders")).scalar()
        product_query = conn.execute(text("SELECT product_id, price, old_price FROM products")).fetchall()
        products = {row.product_id: {"price": row.price, "old_price": row.old_price} for row in product_query}

    return int(max_order_id), products
