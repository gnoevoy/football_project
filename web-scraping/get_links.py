from playwright.sync_api import sync_playwright, Playwright
from helper_functions.links_helpers import *
import requests
import json
import traceback
import logging


# Dictionary to store scraped links for each category
scraped_links = {
    "football_boots": {
        "base_url": "https://www.r-gol.com/en/football-boots?filters=131%5B7502%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C7617%5D%7e152%5B83011%5D",
        "links": [],
    },
    "footballs": {
        "base_url": "https://www.r-gol.com/en/footballs?filters=131%5B83115%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C19117%5D",
        "links": [],
    },
}


def run(playwrigth=Playwright):
    for category, data in scraped_links.items():
        try:
            # Launch browser and block webp images
            browser = playwrigth.chromium.launch(headless=False)
            page = browser.new_page()
            page.route("**/*.{webp}", lambda route: route.abort())

            # Navigate to the first page of the category
            page_num = 1
            url = f"{data['base_url']}&page={page_num}"
            page.goto(url)

            handle_cookies(page)  # Handle cookies pop-up
            total_items = get_total_items(page)  # Get total items in the category
            print(category)

            while True:
                # Scrape product links from the current page
                links = get_product_links(page, page_num)
                data["links"].extend(links)

                # Check the next page's availability
                page_num += 1
                url = f"{data['base_url']}&page={page_num}"
                response = requests.get(url)

                if response.status_code == 200:
                    page.goto(url)
                    page.wait_for_selector("div.category-grid__item")
                else:
                    print("No more pages")
                    break

            # Verify all product links were scraped
            print(f"Total items: {total_items}  |  Scraped links: {len(data['links'])}")
            print()

            browser.close()

        except Exception as e:
            logging.error(traceback.format_exc())


with sync_playwright() as pw:
    run(pw)

# Save scraped links to a JSON file
path_to_file = web_scraping_dir / "data" / "scraped_links.json"

with open(path_to_file, "w") as f:
    json.dump(scraped_links, f, indent=4)
