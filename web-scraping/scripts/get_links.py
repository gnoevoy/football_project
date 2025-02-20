from playwright.sync_api import sync_playwright, Playwright
from pathlib import Path
from dotenv import load_dotenv
import requests
import sys
import os

# Set base path for helper functions
base_path = Path.cwd() / "web-scraping"
sys.path.append(str(base_path))

# Import helper functions
from functions.get_links_helpers import handle_cookies, get_total_items, get_product_links
from functions.db_helpers import get_scraped_ids
from functions.bucket_helpers import load_json_links_to_gcs

# Credentials
load_dotenv(".credentials")

# Dictionary to store scraped links for each category
links = {
    "boots": {
        "base_url": os.getenv("BOOTS_URL"),
        "urls": [],
    },
    "balls": {
        "base_url": os.getenv("BALLS_URL"),
        "urls": [],
    },
}

# Load product data from DB
boots_set, balls_set = get_scraped_ids()


def get_links(logger):

    def run(playwrigth=Playwright):
        logger.info("SCRAPING STARTED ...")

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
                db_data = boots_set if category == "boots" else balls_set

                # Loop through pagination until no more pages are available
                while True:
                    try:
                        # Extract product links from the current page
                        product_links = get_product_links(page, db_data, logger)
                        data["urls"].extend(product_links)
                    except Exception:
                        logger.error(f"Page {page_num} skipped, {url}", exc_info=True)

                    # Move to the next page if available
                    page_num += 1
                    url = f"{data['base_url']}&page={page_num}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        page.goto(url)
                        page.wait_for_selector("div.category-grid__item")
                    else:
                        break  # Stop when no more pages exist

                # Category summary
                logger.info(f"Category: {category.title()}, Total in web-app: {total_items}, Scraped: {len(data["urls"])}")
                browser.close()

            except Exception:
                logger.error("Unexpected error", exc_info=True)

    # Run the scraper using Playwright
    with sync_playwright() as pw:
        run(pw)

    # Save scraped links to a JSON file
    try:
        balls_num = len(links["balls"]["urls"])
        boots_num = len(links["boots"]["urls"])

        # Check if there're new products in web app
        # if so write data and execute next steps in pipeline with the help of specifying boolean flag
        if balls_num + boots_num > 0:
            load_json_links_to_gcs(links)
            logger.info("File was successfully written")
            return False
        else:
            logger.info("No new records in web app")
            return True

    except Exception:
        logger.error(f"Unexpected error", exc_info=True)


if __name__ == "__main__":
    get_links()
