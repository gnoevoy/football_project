from playwright.sync_api import sync_playwright, Playwright
from functions import *
import requests
from pathlib import Path
import json
import pandas as pd


products = []
colors = []
sizes = []
boots_category = []
balls_category = []

json_file_path = web_scraping_folder / "data" / "scraped_links.json"
with open(json_file_path, "r") as f:
    links = json.load(f)

test_data = [links["football_boots"]["links"][1], links["footballs"]["links"][1]]
print(test_data)


def run(playwrigth=Playwright):
    product_id = 1
    category_id = 1

    for category, data in links.items():
        links_lst = data["links"]

    chrome = playwrigth.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.goto(test_data[0])

    # handle cookies + wait for rendering content + open hidden data
    handle_cookies(page)
    main_content = page.locator("div.main-content-wrap")
    main_content.wait_for()
    page.locator("a[aria-controls='long-description-desktop']").click()
    page.locator("a[aria-controls='info-text']").click()

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="main-content-wrap")

    # products
    title = content.find("h1", class_="product-card__title").text
    price = content.find(
        "span",
        class_="text-nowrap price-wrapper price currency product-card__current-price",
    ).text
    description = (
        content.find("div", class_="product-params-content").find("span").contents
    )

    print(title, price)
    print(description)

    # colors

    # sizes

    # catefory features

    # links

    browser.close()


with sync_playwright() as pw:
    run(pw)
