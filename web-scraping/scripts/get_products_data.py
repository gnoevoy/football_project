from playwright.sync_api import sync_playwright, Playwright
from pathlib import Path
from datetime import datetime
import pandas as pd
import json
import sys
import traceback
import logging

# access helper functions
path = Path.cwd() / "web-scraping/"
sys.path.append(str(path))
from helper_functions.links_helpers import handle_cookies
from helper_functions.products_helpers import *


# Initialize lists to store data for CSV files
products, colors, sizes, labels = [], [], [], []
categories, boots_category, balls_category = [], [], []

# Define paths for raw data and product images
raw_data_folder = path / "data" / "raw_data"
images_folder = path / "data" / "product_images"

# Load scraped links from JSON file
json_file_path = path / "data" / "scraped_links.json"
with open(json_file_path, "r") as f:
    links = json.load(f)


def run(playwrigth=Playwright):
    product_id = 1
    category_id = 1

    for category, data in links.items():
        links_lst = data["links"]
        counter = 1
        print(category)
        try:
            # Open browser and navigate to the catalog page
            chrome = playwrigth.chromium
            browser = chrome.launch(headless=False)
            page = browser.new_page()
            page.route("**/*.{webp}", lambda route: route.abort())  # Block webp images
            page.goto(data["base_url"])

            # Determine folder name for storing images
            category_folder = "boots" if category == "football_boots" else "balls"

            # Accept cookies on the website
            handle_cookies(page)

            # Scrape data from each product page
            for link in links_lst:
                size = len(links_lst)

                try:
                    page.goto(link)

                    # Render product page content
                    content = render_product_page(page)

                    # Collect product data and append to the products list
                    item = get_product_data(content, link, product_id, category_id)
                    products.append(item)

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
                    sizes.extend(product_sizes)

                    # Collect category-specific features and append to the appropriate list
                    product_features = get_product_features(content, product_id)
                    if category == "football_boots":
                        boots_category.append(product_features)
                    else:
                        balls_category.append(product_features)

                    # Download and save product images
                    get_product_images(
                        content, link, product_id, images_folder, category_folder
                    )

                    pct = round(counter / size * 100, 2)
                    print(f"Product {counter} of {size}, {pct}% complete.")
                    product_id += 1
                    counter += 1

                except Exception as e:
                    print(f"Error with product link: {link}")
                    logging.error(traceback.format_exc())

            # Add category data to the categories list
            product_category = {
                "category_id": category_id,
                "category_name": category,
                "created_at": datetime.today().strftime("%Y-%m-%d"),
            }
            categories.append(product_category)
            category_id += 1

            print()
            browser.close()

        except Exception as e:
            logging.error(traceback.format_exc())


with sync_playwright() as pw:
    run(pw)


# Save scraped data to CSV files
df_products, df_colors, df_sizes, df_labels = (
    pd.DataFrame(products),
    pd.DataFrame(colors),
    pd.DataFrame(sizes),
    pd.DataFrame(labels),
)

df_categories, boots_category, balls_category = (
    pd.DataFrame(categories),
    pd.DataFrame(boots_category),
    pd.DataFrame(balls_category),
)

# Write data to CSV files with semicolon as the delimiter
df_products.to_csv(raw_data_folder / "products.csv", index=False, sep=";")
df_colors.to_csv(raw_data_folder / "colors.csv", index=False, sep=";")
df_sizes.to_csv(raw_data_folder / "sizes.csv", index=False, sep=";")
df_labels.to_csv(raw_data_folder / "labels.csv", index=False, sep=";")
df_categories.to_csv(raw_data_folder / "categories.csv", index=False, sep=";")
boots_category.to_csv(raw_data_folder / "boots_category.csv", index=False, sep=";")
balls_category.to_csv(raw_data_folder / "balls_category.csv", index=False, sep=";")
