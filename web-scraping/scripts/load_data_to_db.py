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

# Create images table by getting scraped images names
img_dir = web_scraping_dir / "data" / "product_images"
paths = img_dir.rglob("*")
dir_name = "product_images"
images = []

for path in paths:
    if dir_name in path.parts and path.is_file():
        prefix, img = str(path).split("/")[-2:]
        product_id = int(img.split("-")[0])
        image_name = f"{prefix}/{img}"
        is_thumbnail = True if int(img.split("-")[1][0]) == 1 else False

        row = {
            "product_id": product_id,
            "image_name": image_name,
            "is_thumbnail": is_thumbnail,
        }
        images.append(row)

images_df = pd.DataFrame(images)


# connect to database
DB_NAME = "football-project"
USER = "admin"
PASSWORD = "admin"
HOST = "localhost"
PORT = "5432"
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

# list all tables in db
inspector = inspect(engine)
tables = [table for table in inspector.get_table_names() if "ecommerce" in table]
print(tables)


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
