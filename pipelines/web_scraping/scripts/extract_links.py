from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
from pathlib import Path
import requests
import time
import sys
import os

# Add python path and load variables
PIPELINES_DIR = Path(__file__).parents[2]
sys.path.insert(0, str(PIPELINES_DIR))
load_dotenv(PIPELINES_DIR / ".env")

# Import helper functions
from web_scraping.functions.links_helpers import open_catalog, handle_cookies, get_total_items, get_links
from web_scraping.functions.db_helpers import get_scraped_products
from utils.cloud_helpers import load_file_to_bucket

# Dictionary for storing links
dct = {
    "boots": {
        "base_url": os.getenv("BOOTS_URL"),
        "urls": [],
    },
    "balls": {
        "base_url": os.getenv("BALLS_URL"),
        "urls": [],
    },
}


# Run playwright scraper
def scrape_links(logger, playwright=Playwright):
    logger.info("EXTRACTING LINKS ...")

    # Load already existed products from the database to avoid duplicates during scraping
    scraped_boots, scraped_balls = get_scraped_products()

    for category, data in dct.items():
        logger.info(f"Category: {category}")
        scraped_data = scraped_boots if category == "boots" else scraped_balls

        try:
            # Open the catalog page, handle cookies, and get total items in the category
            page_num = 1
            url = f"{data["base_url"]}&page={page_num}"
            page, browser = open_catalog(playwright, url)
            handle_cookies(page)
            total_items = get_total_items(page)

            # Loop through pages and scrape links
            t1_category = time.perf_counter()
            while True:
                try:
                    # Extract links from the current page
                    links, page_total, scraped_num = get_links(page, scraped_data, logger)
                    data["urls"].extend(links)
                    # Summary log about page
                    logger.info(f"Page: {page_num}, scraped: {scraped_num}, items on page: {page_total}")
                except:
                    logger.error(f"Page {page_num} skipped, {url}", exc_info=True)

                # Construct the next page URL
                page_num += 1
                url = f"{data["base_url"]}&page={page_num}"
                response = requests.get(url)

                # Check if the next page is available
                if response.status_code == 200:
                    page.goto(url)
                    page.wait_for_selector("div.category-grid__item")
                else:
                    break

            # Log category summary
            t2_category = time.perf_counter()
            logger.info(f"Category: {category}, scraped: {len(data["urls"])}, total: {total_items}, time: {round(t2_category - t1_category, 2)} seconds")

        except:
            logger.error(f"Category {category} skipped.", exc_info=True)
        finally:
            browser.close()


# Function to upload scraped links to bucket
def load_links_to_bucket(logger):
    # Check if there are new products to upload
    num = len(dct["balls"]["urls"]) + len(dct["boots"]["urls"])

    if num > 0:
        logger.info(f"UPLOADING LINKS TO BUCKET ...")
        load_file_to_bucket(dct, "web-scraping", "links.json", file_type="json")
        logger.info("File was successfully upload to bucket")
        is_empty = False
    else:
        logger.info("Not detected new products in a website")
        is_empty = True

    return is_empty


def extract_links(logger):
    t1 = time.perf_counter()

    # Scrape links and upload to bucket
    with sync_playwright() as pw:
        scrape_links(logger, pw)
    is_empty = load_links_to_bucket(logger)

    # Log execution time
    t2 = time.perf_counter()
    logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
    logger.info("----------------------------------------------------------------")
    return is_empty
