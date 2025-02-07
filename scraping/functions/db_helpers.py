from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv(".credentials")

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
SCHEMA = os.getenv("POSTGRES_SCHEMA")

engine = create_engine(
    f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?options=-csearch_path%3D{SCHEMA}"
)


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
