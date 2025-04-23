from playwright.sync_api import sync_playwright, Playwright
from pathlib import Path
import pandas as pd
import time
import sys

# Add python path
PIPELINES_DIR = Path(__file__).parents[2]
sys.path.insert(0, str(PIPELINES_DIR))

# Import helper functions
from web_scraping.functions.links_helpers import open_catalog, handle_cookies
from web_scraping.functions.data_helpers import render_product_page, get_product, get_sizes, get_details
from web_scraping.functions.db_helpers import get_max_product_id
from utils.cloud_helpers import get_file_from_bucket, load_file_to_bucket

# Initialize variables for storing data
products, sizes, details = [], [], []


# Run playwright scraper
def scrape_data(logger, playwrigth=Playwright):
    logger.info("EXTRACTING DATA ...")
    # Retrieve links from the bucket
    links = get_file_from_bucket("web-scraping", "links.json", file_type="json")
    product_id = get_max_product_id() + 1

    for category, data in links.items():
        logger.info(f"Category: {category}")
        category_id = 1 if category == "boots" else 2
        counter = 0

        # Skip category if no links are available
        if not data["urls"]:
            logger.warning(f"Skipping category {category}, no links")
            continue

        try:
            # Open the catalog page and handle cookie
            page, browser = open_catalog(playwrigth, data["base_url"])
            handle_cookies(page)

            # Loop through links and scrape data
            t1_category = time.perf_counter()
            for url in data["urls"]:
                try:
                    # Render the product page content
                    page.goto(url)
                    content = render_product_page(page)

                    # Scrape core data and additional details
                    # Flags needs for good logging
                    product = get_product(content, url, product_id, category_id)
                    product_sizes, sizes_flag = get_sizes(content, url, product_id, logger)
                    product_details, labels_flag, related_products_flag, features_flag, related_products_message = get_details(content, url, product_id, logger)

                    # Append data to lists
                    products.append(product)
                    sizes.extend(product_sizes)
                    details.append(product_details)

                    # Summary log about product
                    flag = all([sizes_flag, labels_flag, related_products_flag, features_flag])
                    message = "Scraped successfully" if flag else "Scraped with issues"
                    if related_products_message:
                        logger.info(f"{message}, {related_products_message} - {url}")
                    else:
                        logger.info(f"{message} - {url}")
                    product_id += 1
                    counter += 1

                except:
                    logger.error(f"Product was skipped, {url}", exc_info=True)

            # Log category summary
            t2_category = time.perf_counter()
            logger.info(f"Category: {category}, scraped: {counter}, total: {len(data["urls"])}, time: {round(t2_category - t1_category, 2)} seconds")
        except:
            logger.error(f"Category {category} skipped.", exc_info=True)
        finally:
            browser.close()


# Upload all lists to the bucket
def upload_to_bucket(logger):
    logger.info(f"UPLOADING DATA TO BUCKET ...")
    bucket_dir = "web-scraping/raw"
    load_file_to_bucket(pd.DataFrame(products), bucket_dir, "products", file_type="csv")
    load_file_to_bucket(pd.DataFrame(sizes), bucket_dir, "sizes", file_type="csv")
    load_file_to_bucket(details, bucket_dir, "details.json", file_type="json")
    logger.info("Files were successfully uploaded to bucket")


def extract_data(logger):
    try:
        t1 = time.perf_counter()

        # Get links, scrape product pages and upload data to bucket
        with sync_playwright() as pw:
            scrape_data(logger, pw)
        upload_to_bucket(logger)

        # Log execution time
        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
    except:
        logger.error(f"", exc_info=True)
