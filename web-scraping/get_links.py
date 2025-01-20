from playwright.sync_api import sync_playwright, Playwright
from functions import *
import requests
import json
from pathlib import Path


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

        # open catalog page
        chrome = playwrigth.chromium
        browser = chrome.launch(headless=False)
        page = browser.new_page()
        page.route("**/*.{webp}", lambda route: route.abort())

        # construct start page
        page_num = 1
        base_url = data["base_url"]
        url = f"{base_url}&page={page_num}"
        page.goto(url)

        # handle cookies window
        handle_cookies(page)

        # total items
        total_items = get_total_items(page)
        print(f"category: {category}")

        # loop over pages
        while True:
            # scrape links from product cards
            links, products = get_product_links(page)
            data["links"].extend(links)
            print(f"page: {page_num} | items: {len(products)} | scraped: {len(links)}")

            # handle pagination via status code of page
            page_num += 1
            url = f"{base_url}&page={page_num}"

            if not pagination(page, url):
                print("No more pages")
                break

        print("====================================")
        print(f"total items: {total_items} | scraped: {len(data["links"])}")
        print()
        browser.close()


with sync_playwright() as pw:
    run(pw)

# # file path
# p = Path.cwd() / "web-scraping" / "data" / "scraped_links.json"

# with open(p, "w") as f:
#     json.dump(scraped_links, f)
#     print("Data successfully saved to file!")
