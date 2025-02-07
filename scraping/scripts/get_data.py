from playwright.sync_api import sync_playwright, Playwright
from pathlib import Path
import requests
from datetime import date
import sys
import json
import traceback

# Set base path for helper functions
base_path = Path.cwd() / "scraping"
sys.path.append(str(base_path))

# Import helper functions
from functions.get_links_helpers import handle_cookies
from functions.get_data_helpers import *
from functions.db_helpers import get_max_product_id
from functions.logs import logs_setup

# Setup logging
logging_msg = logs_setup("get_data.log")

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
product_features = {}


def run(playwrigth=Playwright):
    logging_msg.info("==========    Scraping started   ==========")

    max_product_id = get_max_product_id()
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

            for url in urls_lst[:5]:
                try:
                    # Render product page content
                    page.goto(url)
                    content = render_product_page(page)

                    # Collect product data and append to the products list
                    product = get_product_data(content, url, product_id, category_id)
                    products.append(product)

                    # Collect color data and append to the colors list
                    product_colors = get_product_colors(content, product_id)
                    if product_colors:
                        colors.extend(product_colors)

                    # Collect labels data and append it to lables list
                    product_labels = get_product_labels(content, product_id)
                    if product_labels:
                        labels.extend(product_labels)

                    # Collect size data and append to the sizes list
                    product_sizes = get_product_sizes(content, product_id)
                    if product_sizes:
                        sizes.extend(product_sizes)

                    product_id += 1
                    scraped_products_num += 1

                except Exception as e:
                    traceback.print_exc()
                    logging_msg.error(f"Skipping product: {url}", exc_info=True)

            print(colors)
            print(labels)
            print(sizes)

            # Log category summary
            category_message = {
                "scraped_products": scraped_products_num,
                "total_links": len(urls_lst),
            }
            print(category_message)
            logging_msg.info(category_message)

        except Exception as e:
            traceback.print_exc()
            logging_msg.error("An error occurred:", exc_info=True)

        browser.close()


with sync_playwright() as pw:
    run(pw)

# Write scraped data to CSV files
