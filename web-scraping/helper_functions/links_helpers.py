from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import re


web_scraping_folder = Path.cwd() / "web-scraping"


def handle_cookies(page):
    cookie = page.locator("div.CybotCookiebotDialogActive")
    cookie.wait_for()
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")


def get_total_items(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    total = soup.find("p", class_="products-list-controls-container__paragraph amount")
    return int(total.text)


def get_product_links(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    grid = soup.find("div", class_="category-grid category-grid--small-items")
    products = grid.select("div.category-grid__item:not(.last-brick)")
    links = grid.find_all("a", class_=re.compile(r"\bproduct-item product-brick\b"))
    page_links = [link["href"] for link in links]

    return page_links, products


def pagination(page, url):
    response = requests.get(url)

    if response.status_code == 200:
        page.goto(url)
        page.wait_for_selector("div.category-grid__item")
        return True
    else:
        return False


if __name__ == "__main__":
    pass
