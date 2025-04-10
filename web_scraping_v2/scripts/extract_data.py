from playwright.sync_api import sync_playwright, Playwright
from pathlib import Path
import pandas as pd
import time
import sys


# add python path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# import helper functions
from functions.links_helpers import open_catalog, handle_cookies
from functions.data_helpers import render_product_page, get_product, get_sizes, get_details
from functions.db_helpers import get_max_product_id
from functions.bucket_helpers import get_file_from_bucket, load_file_to_bucket

# initialize variable for storing data
products, sizes, details = [], [], []


# run scraper
def scrape_data(logger, playwrigth=Playwright):
    logger.info("EXTRACTING DATA ...")
    # get links from bucket
    links = get_file_from_bucket("web-scraping", "links.json", file_type="json")
    product_id = get_max_product_id() + 1

    for category, data in links.items():
        logger.info(f"Category: {category}")
        category_id = 1 if category == "boots" else 2
        counter = 0

        # handle case when no links in category
        if not data["urls"]:
            logger.warning(f"Skipping category {category}, no links")
            continue

        try:
            # open catalog and handle cookies
            page, browser = open_catalog(playwrigth, data["base_url"])
            handle_cookies(page)

            # loop through links and scrape data
            t1_category = time.perf_counter()
            for url in data["urls"][:3]:
                try:
                    # render product page content
                    page.goto(url)
                    content = render_product_page(page)

                    # scrape core data for product, if successful try to scrape additional data, else skip item
                    # flags needed to check if item was scraped fully or not
                    product = get_product(content, url, product_id, category_id)
                    product_sizes, sizes_flag = get_sizes(content, url, product_id, logger)
                    product_details, labels_flag, related_products_flag, features_flag = get_details(content, url, product_id, logger)

                    # add values to lists
                    products.append(product)
                    sizes.extend(product_sizes)
                    details.append(product_details)

                    # summary log about a product
                    flag = all([sizes_flag, labels_flag, related_products_flag, features_flag])
                    message = "Scraped successfully" if flag else "Scraped with issues"
                    logger.info(f"{message}, {url}")
                    product_id += 1
                    counter += 1

                except:
                    logger.error(f"Product was skipped, {url}", exc_info=True)

            # category summary
            t2_category = time.perf_counter()
            logger.info(f"Category: {category}, scraped: {counter}, total: {len(data["urls"])}, time: {round(t2_category - t1_category, 2)} seconds")

        except:
            logger.error(f"Category {category} skipped.", exc_info=True)
        finally:
            browser.close()


# load lists to bucket
def upload_to_bucket(logger):
    logger.info(f"UPLOADING DATA TO BUCKET ...")
    bucket_dir = "web-scraping/raw"
    load_file_to_bucket(pd.DataFrame(products), bucket_dir, "products", file_type="csv")
    load_file_to_bucket(pd.DataFrame(sizes), bucket_dir, "sizes", file_type="csv")
    load_file_to_bucket(details, bucket_dir, "details.json", file_type="json")
    logger.info("Files were successfully uploaded to bucket")


# main logic (scrape product pages -> write data to lists -> load to bucket)
def extract_data(logger):
    try:
        t1 = time.perf_counter()

        with sync_playwright() as pw:
            scrape_data(logger, pw)

        upload_to_bucket(logger)

        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
    except:
        logger.error(f"", exc_info=True)
