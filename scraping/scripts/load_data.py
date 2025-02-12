from pathlib import Path
import sys
import traceback

# Set base path for helper functions and paths
base_path = Path.cwd() / "scraping"
sys.path.append(str(base_path))
from functions.logs import logs_setup
from functions.db_helpers import * 

# Define paths
data_dir = base_path / "data"
clean_data_path = data_dir / "cleaned"
img_dir = base_path / "data" / "img"

# Setup logging
logger = logs_setup("load_data.log")

try:
    # Load data to postgres db and update summary table
    load_to_db("products", clean_data_path, "products.csv")
    load_to_db("sizes", clean_data_path, "sizes.csv")
    load_to_db("colors", clean_data_path, "colors.csv")
    load_to_db("labels", clean_data_path, "labels.csv")
    logger.info("Data successfully loaded to postgres db")

    # Update summary table
    update_summary_table()
    logger.info("Summary table successfully updated")

    # Load json file to mongo db
    features_num = load_to_mongo_db(clean_data_path)
    logger.info(f"{features_num} records successfully loaded to mongo db")
    
    # Load images to google storage
    images_num = upload_images_to_storage(img_dir)
    logger.info(f"{images_num} images successfully loaded to storage")

except Exception:
    logger.error("Unexpected error", exc_info=True)

logger.info("----------")
