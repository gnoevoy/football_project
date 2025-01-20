from playwright.sync_api import sync_playwright, Playwright
from functions import *
import requests


base_url = "https://www.r-gol.com/en/football-boots?filters=131%5B7502%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C7617%5D%7e152%5B83011%5D"
boots = []


def run(playwrigth=Playwright):
    # open catalog page
    chrome = playwrigth.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.route("**/*.{webp}", lambda route: route.abort())

    # construct start page
    page_num = 11
    url = f"{base_url}&page={page_num}"
    page.goto(url)

    # handle cookies window
    handle_cookies(page)

    # total items
    total_items = get_total_items(page)

    # loop over pages
    while True:
        # scrape links from product cards
        links, products = get_product_links(page)
        boots.extend(links)
        print(f"page: {page_num} | items: {len(products)} | scraped: {len(links)}")

        # handle pagination via status code of page
        page_num += 1
        url = f"{base_url}&page={page_num}"

        if not pagination(page, url):
            print("No more pages")
            break

    print("====================================")
    print(f"total items: {total_items} | scraped: {len(boots)}")
    browser.close()


with sync_playwright() as pw:
    run(pw)
