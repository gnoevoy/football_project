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
from functions.db_helpers import get_scraped_ids
from functions.logs import logs_setup

# Setup logging
logging_msg = logs_setup("get_links.log")

# Dictionary to store scraped links for each category
links = {
    "boots": {
        "base_url": "https://www.r-gol.com/en/football-boots?filters=131%5B7502%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C7617%5D%7e152%5B83011%5D",
        "urls": [],
    },
    "balls": {
        "base_url": "https://www.r-gol.com/en/footballs?filters=131%5B83115%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C19117%5D",
        "urls": [],
    },
}

# Load product data from DB
boots_db, balls_db = get_scraped_ids()


def run(playwrigth=Playwright):
    logging_msg.info("==========    Scraping started   ==========")

    for category, data in links.items():
        try:
            # Launch browser with image blocking
            browser = playwrigth.chromium.launch(headless=False)
            page = browser.new_page()
            page.route("**/*.{webp,png,jpeg,jpg}", lambda route: route.abort())

            # Open the first category page
            page_num = 1
            url = f"{data['base_url']}&page={page_num}"
            page.goto(url)

            handle_cookies(page)  # Dismiss cookie pop-ups

            total_items = get_total_items(page)  # Count total products in category
            db_data = boots_db if category == "boots" else balls_db
            skipped_pages = 0

            # Loop through pagination until no more pages are available
            while True:
                try:
                    # Extract product links from the current page
                    product_links = get_product_links(page, db_data)
                    data["urls"].extend(product_links)
                except Exception as e:
                    skipped_pages += 1
                    traceback.print_exc()
                    logging_msg.warning("Page skipped due to error", exc_info=True)

                # Move to the next page if available
                page_num += 1
                url = f"{data['base_url']}&page={page_num}"
                response = requests.get(url)

                if response.status_code == 200:
                    page.goto(url)
                    page.wait_for_selector("div.category-grid__item")
                else:
                    break  # Stop when no more pages exist

            # Log scraping summary for the category
            message = {
                "category": category,
                "scraped_urls": len(data["urls"]),
                "db_data": len(db_data),
                "app_data": total_items,
                "skipped_pages": skipped_pages,
            }
            print(message)
            logging_msg.info(message)
            browser.close()

        except Exception as e:
            traceback.print_exc()
            logging_msg.error("An error occurred:", exc_info=True)


# Run the scraper using Playwright
with sync_playwright() as pw:
    run(pw)


# Save scraped links to a JSON file
file_path = base_path / "data" / "scraped_links.json"

with open(file_path, "w") as f:
    json.dump(links, f, indent=4)
