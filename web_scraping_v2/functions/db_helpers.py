from sqlalchemy import text
from pathlib import Path
import sys

# add python path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# import connections
from utils.connections import engine


def get_scraped_products():
    with engine.connect() as conn:
        boots_query = conn.execute(text("SELECT scraped_id FROM products WHERE category_id = 1"))
        balls_query = conn.execute(text("SELECT scraped_id FROM products WHERE category_id = 2"))
        boots = boots_query.scalars().all()
        balls = balls_query.scalars().all()

    return boots, balls


def get_max_product_id():
    with engine.connect() as conn:
        max_product_id = conn.execute(text("SELECT COALESCE(MAX(product_id), 0) FROM products"))
        num = max_product_id.scalar()
    return num
