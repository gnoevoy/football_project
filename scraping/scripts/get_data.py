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
from functions.get_links_helpers import *
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

        try:
            # Launch browser with image blocking
            browser = playwrigth.chromium.launch(headless=False)
            page = browser.new_page()
            page.route("**/*.{webp,png,jpeg,jpg}", lambda route: route.abort())
            page.goto(data["base_url"])
            handle_cookies(page)  # Dismiss cookie pop-ups

            # Determine folder name for storing images
            category_folder = "boots" if category == "boots" else "balls"

            for url in urls_lst:
                pass

            logging_msg.info("good")

        except Exception as e:
            traceback.print_exc()
            logging_msg.error("An error occurred:", exc_info=True)


with sync_playwright() as pw:
    run(pw)


# Write scraped data to CSV files
