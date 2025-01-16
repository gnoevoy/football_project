from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup


# first test pagination
# get all available links from my catalog


def get_links(playwrigth: Playwright):
    url = "https://www.r-gol.com/en/football-boots?filters=131%5B7502%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C7617%5D%7e152%5B83011%5D&page=13"
    chrome = playwrigth.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.route("**/*.{webp}", lambda route: route.abort())
    page.goto(url)

    # handle cookie pop up window
    cookie_pop_up = page.locator("div.CybotCookiebotDialogActive")
    cookie_pop_up.wait_for()
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")

    while True:
        page.wait_for_selector("div.category-grid__item")
        html_content = page.content()
        soup = BeautifulSoup(html_content, "html.parser")

        # scrape links
        cards = soup.find_all("a", class_="product-item product-brick")
        for x in cards:
            print(x["href"])

        num = len(cards)

        print(f"{num} -- {page.url}")

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
