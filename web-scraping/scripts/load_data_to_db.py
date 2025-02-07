from sqlalchemy import create_engine, inspect
from pathlib import Path
import pandas as pd

# import cleaned csv files
web_scraping_dir = Path.cwd() / "web-scraping"
data_dir = web_scraping_dir / "data" / "cleaned_data"

products_df = pd.read_csv(data_dir / "products.csv", delimiter=";")
colors_df = pd.read_csv(data_dir / "colors.csv", delimiter=";")
sizes_df = pd.read_csv(data_dir / "sizes.csv", delimiter=";")
labels_df = pd.read_csv(data_dir / "labels.csv", delimiter=";")
categories_df = pd.read_csv(data_dir / "categories.csv", delimiter=";")
boots_category_df = pd.read_csv(data_dir / "boots_category.csv", delimiter=";")
balls_category_df = pd.read_csv(data_dir / "balls_category.csv", delimiter=";")
images_df = pd.read_csv(data_dir / "images.csv", delimiter=";")

# connect to database
DB_NAME = "football-project"
USER = "admin"
PASSWORD = "admin"
HOST = "localhost"
PORT = "5432"
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

# # list all tables in db
# inspector = inspect(engine)
# tables = [table for table in inspector.get_table_names() if "ecommerce" in table]
# print(tables)


# load data to db
def load_to_db(table_name, df):
    df.to_sql(table_name, engine, if_exists="append", index=False)


try:
    load_to_db("ecommerce_categories", categories_df)
    load_to_db("ecommerce_product", products_df)
    load_to_db("ecommerce_colors", colors_df)
    load_to_db("ecommerce_sizes", sizes_df)
    load_to_db("ecommerce_labels", labels_df)
    load_to_db("ecommerce_balls_features", balls_category_df)
    load_to_db("ecommerce_boots_features", boots_category_df)
    load_to_db("ecommerce_product_images", images_df)
except Exception as e:
    print(e)
