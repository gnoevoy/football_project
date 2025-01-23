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

# open scraped links
json_file_path = web_scraping_folder / "data" / "scraped_links.json"
with open(json_file_path, "r") as f:
    links = json.load(f)


def run(playwrigth=Playwright):
    product_id = 1
    category_id = 1

    for category, data in links.items():
        links_lst = data["links"]

        # open browser at catalog page
        chrome = playwrigth.chromium
        browser = chrome.launch(headless=False)
        page = browser.new_page()
        page.goto(data["base_url"])

        # handle cookies
        handle_cookies(page)

        for link in links_lst[:1]:
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

            product_id += 1

        # add data to categories table
        product_gategory = {"category_id": category_id, "category_name": category}
        categories.append(product_gategory)
        category_id += 1

        browser.close()

    print(boots_category)
    print(balls_category)


with sync_playwright() as pw:
    run(pw)
