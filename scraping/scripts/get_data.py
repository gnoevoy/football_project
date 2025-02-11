from playwright.sync_api import sync_playwright, Playwright
from pathlib import Path
import sys
import json


# Set base path for helper functions
base_path = Path.cwd() / "scraping"
sys.path.append(str(base_path))

# Import helper functions
from functions.get_links_helpers import handle_cookies
from functions.get_data_helpers import *
from functions.db_helpers import get_max_product_id
from functions.logs import logs_setup

# Setup logging
logger = logs_setup("get_data.log")

# Define paths
data_dir = base_path / "data"
raw_data_path = data_dir / "raw"
img_dir = data_dir / "img"
json_file_path = data_dir / "scraped_links.json"

# Load scraped links from JSON file
with open(json_file_path, "r") as f:
    links = json.load(f)

# Initialize lists to store data for CSV files
products, colors, sizes, labels = [], [], [], []
product_features = {"product_id": "features_dct"}


def run(playwrigth=Playwright):
    logger.info("SCRAPING STARTED")
    max_product_id = get_max_product_id()  # Get the highest product_id from db
    product_id = max_product_id + 1

    for category, data in links.items():
        urls_lst = data["urls"]
        scraped_products_num = 0
        category_id = 1 if category == "boots" else 2

        try:
            # Launch browser with image blocking
            browser = playwrigth.chromium.launch(headless=False)
            page = browser.new_page()
            page.route("**/*.{webp,png,jpeg,jpg}", lambda route: route.abort())
            page.goto(data["base_url"])
            handle_cookies(page)  # Dismiss cookie pop-ups

            # Determine folder name for storing images
            category_folder = "boots" if category == "boots" else "balls"
            logger.info("----------")
            logger.info(f"{category.upper()}")

            for url in urls_lst:
                try:
                    # Render product page content
                    page.goto(url)
                    content = render_product_page(page)

                    # Scrape main product data (if this fails -> skip such a product)
                    product = get_product_data(content, url, product_id, category_id)
                    products.append(product)

                    # Collect color data and append to the colors list
                    product_colors, flag_colors = get_product_colors(
                        content, product_id, url, logger
                    )
                    colors.extend(product_colors)

                    # Collect labels data and append it to lables list
                    product_labels, flag_labels = get_product_labels(
                        content, product_id, url, logger
                    )
                    labels.extend(product_labels)

                    # Collect size data and append to the sizes list
                    product_sizes, flag_sizes = get_product_sizes(
                        content, product_id, url, logger
                    )
                    sizes.extend(product_sizes)

                    # Collect product specific features
                    features, flag_features = get_product_features(
                        content, product_id, url, logger
                    )
                    if features:
                        product_features[product_id] = features

                    # Download and save product images
                    flag_images = get_product_images(
                        content, product_id, img_dir, category_folder, url, logger
                    )

                    # Check if all data were scraped successfully
                    success = [
                        flag_colors,
                        flag_labels,
                        flag_sizes,
                        flag_features,
                        flag_images,
                    ]
                    if all(success):
                        logger.info(f"Product {product_id} scraped successfully")

                    product_id += 1
                    scraped_products_num += 1

                except Exception:
                    logger.error(f"Product was skipped, {url}", exc_info=True)

            # Category summary
            logger.info(f"Scraped: {scraped_products_num} | Total: {len(urls_lst)}")

        except Exception:
            logger.error("Unexpected error", exc_info=True)

        browser.close()


with sync_playwright() as pw:
    run(pw)


# Write scraped data to CSV / JSON files
logger.info("----------")
logger.info("OUTPUT")
try:
    export_to_csv(products, raw_data_path, "products.csv")
    export_to_csv(labels, raw_data_path, "labels.csv")
    export_to_csv(colors, raw_data_path, "colors.csv")
    export_to_csv(sizes, raw_data_path, "sizes.csv")

    with open(raw_data_path / "product_features.json", "w") as f:
        json.dump(product_features, f, indent=4)

    logger.info("Files were successfully written")

except Exception:
    logger.error(f"Unexpected error", exc_info=True)
logger.info("----------")
