from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()  # fake user-agents
product_links = []


def get_links(playwrigth: Playwright):
    url = "https://www.r-gol.com/en/football-boots?filters=131%5B7502%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C7617%5D%7e152%5B83011%5D"
    chrome = playwrigth.chromium
    browser = chrome.launch(headless=False)
    context = browser.new_context(user_agent=ua.random)
    page = browser.new_page()
    page.route("**/*.{webp}", lambda route: route.abort())
    page.goto(url)

    while True:
        html_content = page.content()
        soup = BeautifulSoup(html_content, "html.parser")
        links = soup.select("a.product-item.product-brick")

        for link in links[:1]:
            product_links.append(link["href"])

        next_page = page.locator("div[class='category-grid__item.last-brick']")

        if next_page:
            print("found")
            page.locator("div[class='category-grid__item.last-brick']").click()
        else:
            print("not found")
            break

    browser.close()


with sync_playwright() as pw:
    get_links(pw)


print(product_links)
