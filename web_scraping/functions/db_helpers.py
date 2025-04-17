from sqlalchemy import text
from pathlib import Path
import sys

# Add python path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# Import db's connections
from utils.connections import engine, mongo_collection


# Helper for exrtract_links.py
def get_scraped_products():
    with engine.connect() as conn:
        boots_query = conn.execute(text("SELECT scraped_id FROM products WHERE category_id = 1"))
        balls_query = conn.execute(text("SELECT scraped_id FROM products WHERE category_id = 2"))
        boots = boots_query.scalars().all()
        balls = balls_query.scalars().all()
    return boots, balls


# Helper for extract_data.py
def get_max_product_id():
    with engine.connect() as conn:
        max_product_id = conn.execute(text("SELECT COALESCE(MAX(product_id), 0) FROM products"))
        num = max_product_id.scalar()
    return num


# Helper for transform_data.py
def load_to_postgre(df, table_name):
    df.to_sql(table_name, engine, if_exists="append", index=False)


# Helper for transform_data.py
def load_to_mongo(lst):
    mongo_collection.insert_many(lst)
    return len(lst)


# Update summary table, track how many records were added from scraping
def update_summary_table(boots, balls):
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM products"))
        total_num = total.scalar()
        row = {"total": total_num if total_num else 0, "new_boots": boots, "new_balls": balls}

        # Insert record and commit changes
        query = text("INSERT INTO summary (total, new_boots, new_balls) VALUES (:total, :new_boots, :new_balls)")
        conn.execute(query, row)
        conn.commit()
