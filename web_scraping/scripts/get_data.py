from playwright.sync_api import sync_playwright, Playwright
from pathlib import Path
import pandas as pd
import sys

# Set base path for helper functions
WEB_SCRAPING_DIR = Path(__file__).parent.parent
sys.path.append(str(WEB_SCRAPING_DIR))

# Import helper functions
from functions.get_links_helpers import handle_cookies
from functions.get_data_helpers import *
from functions.db_helpers import get_max_product_id
from functions.bucket_helpers import get_links_from_gcs, load_file_to_gcs
from functions.bucket_helpers import delete_blobs_from_gcs


def scrape_data(logger):
    # Load scraped links from JSON file
    links = get_links_from_gcs()

    # Delete image from bucket before scraping new products
    delete_blobs_from_gcs()

    # Initialize lists to store data for CSV files
    products, colors, sizes, labels, images = [], [], [], [], []
    features = {}

    def run(playwrigth=Playwright):
        logger.info("DATA SCRAPING STARTED")
        max_product_id = get_max_product_id()  # Get the highest product_id from db
        product_id = max_product_id + 1

        for category, data in links.items():
            urls_lst = data["urls"]
            category_id = 1 if category == "boots" else 2
            counter = 0

            # Handle case when list is empty (no links)
            if not urls_lst:
                logger.warning(f"Skipping category {category.title()} - no url's found.")
                continue

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
                    try:
                        # Render product page content
                        page.goto(url)
                        content = render_product_page(page)

                        # Scrape main product data (if this fails, skip the product)
                        product = get_product_data(content, url, product_id, category_id)
                        products.append(product)

                        # Extract and store product-related data
                        # Flags variables help to indicate whether data was fully scraped or not
                        product_colors, flag_colors = get_product_colors(content, product_id, url, logger)
                        colors.extend(product_colors)

                        product_labels, flag_labels = get_product_labels(content, product_id, url, logger)
                        labels.extend(product_labels)

                        product_sizes, flag_sizes = get_product_sizes(content, product_id, url, logger)
                        sizes.extend(product_sizes)

                        product_features, flag_features = get_product_features(content, url, logger)
                        if product_features:
                            features[product_id] = product_features

                        # Download and save product images
                        product_images, flag_images = get_product_images(content, product_id, category_folder, url, logger)
                        images.extend(product_images)

                        # Validate if all data was successfully scraped
                        flags = [flag_colors, flag_labels, flag_sizes, flag_features, flag_images]
                        if all(flags):
                            logger.info(f"Product {product_id} scraped successfully")
                        else:
                            logger.warning(f"Product {product_id} has missing / corrupted data, {url}")

                        product_id += 1
                        counter += 1

                    except Exception:
                        logger.error(f"Product was skipped, {url}", exc_info=True)

                # Category summary
                logger.info(f"Category: {category.title()}, Total: {len(urls_lst)}, Scraped: {counter}")
                logger.info("")

            except Exception:
                logger.error("Unexpected error", exc_info=True)

            browser.close()

    with sync_playwright() as pw:
        run(pw)

    # Load scraped data to bucket
    try:
        raw_files_dir = "web-scraping/raw"
        load_file_to_gcs(pd.DataFrame(products), raw_files_dir, "products.csv")
        load_file_to_gcs(pd.DataFrame(labels), raw_files_dir, "labels.csv")
        load_file_to_gcs(pd.DataFrame(colors), raw_files_dir, "colors.csv")
        load_file_to_gcs(pd.DataFrame(sizes), raw_files_dir, "sizes.csv")
        load_file_to_gcs(pd.DataFrame(images), raw_files_dir, "images.csv")
        load_file_to_gcs(features, raw_files_dir, "features.json", csv=False)
        logger.info("Files were successfully written to bucket")
        logger.info("")

    except Exception:
        logger.error(f"Unexpected error", exc_info=True)
        logger.info("")


if __name__ == "__main__":
    scrape_data()
