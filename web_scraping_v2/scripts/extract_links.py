from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
from pathlib import Path
import requests
import time
import sys
import os


# add python path and load variables
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

# import helper functions
from functions.links_helpers import open_catalog, handle_cookies, get_total_items, get_links
from functions.db_helpers import get_scraped_products
from functions.bucket_helpers import load_file_to_bucket

# dictionary for storing links
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


# run scraper
def scrape_links(logger, playwrigth=Playwright):
    logger.info("EXTRACTING LINKS ...")

    # load product from DB to avoid scraping already existing products
    scraped_boots, scraped_balls = get_scraped_products()

    for category, data in dct.items():
        logger.info(f"Category: {category}")
        scraped_data = scraped_boots if category == "boots" else scraped_balls

        try:
            # open catalog, handle cookies and retrieve num of products in category
            page_num = 1
            url = f"{data["base_url"]}&page={page_num}"
            page, browser = open_catalog(playwrigth, url)
            handle_cookies(page)
            total_items = get_total_items(page)

            # loop through pages and scrape links
            t1_category = time.perf_counter()
            while True:
                try:
                    links, page_total, scraped_num = get_links(page, scraped_data, logger)
                    data["urls"].extend(links)
                    # page summmary
                    logger.info(f"Page: {page_num}, scraped: {scraped_num}, items on page: {page_total}")
                except Exception:
                    logger.error(f"Page {page_num} skipped, {url}", exc_info=True)

                # construct next page URL
                page_num += 1
                url = f"{data["base_url"]}&page={page_num}"
                response = requests.get(url)

                # check if the page is available
                if response.status_code == 200:
                    page.goto(url)
                    page.wait_for_selector("div.category-grid__item")
                else:
                    break

            # category summary
            t2_category = time.perf_counter()
            logger.info(f"Category: {category}, scraped: {len(data["urls"])}, total: {total_items}, time: {round(t2_category - t1_category, 2)} seconds")

        except:
            logger.error(f"Category {category} skipped.", exc_info=True)
        finally:
            browser.close()


def load_links_to_bucket(logger):
    # check if there are new products in the website, if so load links to bucket
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


# main logic (run scraper -> write data to dct -> load to bucket)
def extract_links(logger):
    try:
        t1 = time.perf_counter()

        with sync_playwright() as pw:
            scrape_links(logger, pw)

        is_empty = load_links_to_bucket(logger)

        t2 = time.perf_counter()
        logger.info(f"Finished in {round(t2 - t1, 2)} seconds")
        logger.info("----------------------------------------------------------------")
        return is_empty
    except:
        logger.error(f"", exc_info=True)


if __name__ == "__main__":
    extract_links()
