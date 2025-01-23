from playwright.sync_api import sync_playwright, Playwright
from helper_functions.links_helpers import handle_cookies, web_scraping_folder
from helper_functions.products_helpers import *
import requests
from pathlib import Path
import json
import pandas as pd

# tabel for db
products = []
colors = []
sizes = []
categories = []
boots_category = []
balls_category = []

# path to raw_data
raw_data_folder = web_scraping_folder / "data" / "raw_data"

# path to product images
images_folder = web_scraping_folder / "data" / "images"

# open scraped links
json_file_path = web_scraping_folder / "data" / "scraped_links.json"
with open(json_file_path, "r") as f:
    links = json.load(f)


def run(playwrigth=Playwright):
    product_id = 1
    category_id = 1

    for category, data in links.items():
        links_lst = data["links"]

        # images folder
        category_folder = "boots" if category == "football_boots" else "balls"

        # open browser at catalog page
        chrome = playwrigth.chromium
        browser = chrome.launch(headless=False)
        page = browser.new_page()
        page.goto(data["base_url"])

        # handle cookies
        handle_cookies(page)

        for link in links_lst[:5]:
            page.goto(link)

            # render all content on the page
            content = render_product_page(page)

            # add data to products table
            item = get_product_data(content, link, product_id, category_id)
            products.append(item)

            # add data to colors table
            product_colors = get_product_colors(content, product_id)
            if product_colors:
                colors.extend(product_colors)

            # add data to sizes table
            product_sizes = get_product_sizes(content, product_id)
            sizes.extend(product_sizes)

            # add data to category features
            product_features = get_product_features(content, product_id)
            if category == "football_boots":
                boots_category.append(product_features)
            else:
                balls_category.append(product_features)

            # upload images of product
            get_product_images(
                content, link, product_id, images_folder, category_folder
            )

            product_id += 1

        # add data to categories table
        product_gategory = {"category_id": category_id, "category_name": category}
        categories.append(product_gategory)
        category_id += 1

        browser.close()


with sync_playwright() as pw:
    run(pw)


# store data in csv files
pd.DataFrame(products).to_csv(raw_data_folder / "products.csv", index=False)
pd.DataFrame(colors).to_csv(raw_data_folder / "colors.csv", index=False)
pd.DataFrame(sizes).to_csv(raw_data_folder / "sizes.csv", index=False)
pd.DataFrame(categories).to_csv(raw_data_folder / "categories.csv", index=False)
pd.DataFrame(boots_category).to_csv(raw_data_folder / "boots_category.csv", index=False)
pd.DataFrame(balls_category).to_csv(raw_data_folder / "balls_category.csv", index=False)
