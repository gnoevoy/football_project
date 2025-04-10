from sqlalchemy import text
from pathlib import Path
import sys

# Set base path for helper functions
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# import db connections
from utils.connections import engine, mongo_collection


# Retrieve already scraped products ids
def get_scraped_products():
    with engine.connect() as conn:
        products = conn.execute(text("SELECT category_id, scraped_id FROM products"))
        dct = products.mappings().all()

        res = {"boots": [], "balls": []}
        for row in dct:
            if row["category_id"] == 1:
                res["boots"].append(row["scraped_id"])
            else:
                res["balls"].append(row["scraped_id"])
        return res


# Get the highest product id from db
def get_max_product_id():
    with engine.connect() as conn:
        max_product_id = conn.execute(text("SELECT COALESCE(MAX(product_id), 0) FROM products"))
        num = max_product_id.scalar()
    return num


# Load dataframe to db if there're records in dataframe
def load_to_db(df, table_name):
    if len(df) > 0:
        df.to_sql(table_name, engine, if_exists="append", index=False)


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
    return boots + balls


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

        product_sizes = conn.execute(text("SELECT product_id, size FROM sizes WHERE in_stock IS TRUE")).mappings().all()
        sizes = {}
        for row in product_sizes:
            if row["product_id"] not in sizes:
                sizes[row["product_id"]] = [row["size"]]
            else:
                sizes[row["product_id"]].append(row["size"])

    return int(max_order_id), products, sizes
