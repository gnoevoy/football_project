from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import re

ua = UserAgent()  # fake user-agents
product_links = set()


def get_links(playwrigth=Playwright):
    url = "https://www.r-gol.com/en/football-boots?filters=131%5B7502%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C7617%5D%7e152%5B83011%5D"
    chrome = playwrigth.chromium
    browser = chrome.launch(headless=False)
    context = browser.new_context(user_agent=ua.random)
    page = browser.new_page()
    page.route("**/*.{webp}", lambda route: route.abort())
    page.goto(url)

    # handle cookie pop up window
    cookie_pop_up = page.locator("div.CybotCookiebotDialogActive")
    cookie_pop_up.wait_for()
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")

    # handle lazy loading
    # page.keyboard.press("End")
    # page.wait_for_selector("div.category-grid__item")

    while True:
        html_content = page.content()
        soup = BeautifulSoup(html_content, "html.parser")

        # scraping links
        cards = soup.find_all("div", class_="category-grid__item")
        for item in cards:
            url = item.find("a", class_=re.compile("product-item"))
            if url:
                product_links.add(url["href"])

        # handle pagination
        next_page = soup.find("div", class_="category-grid__item last-brick")

        if next_page:
            page.locator("div.category-grid__item.last-brick").click()
        else:
            print("no more pages")
            break

    browser.close()


with sync_playwright() as pw:
    get_links(pw)


print(f"aim: 440 - result: {len(product_links)}")
