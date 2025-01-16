from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup


# first test pagination
# get all available links from my catalog


def get_links(playwrigth: Playwright):
    url = "https://www.r-gol.com/en/football-boots?filters=131%5B7502%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C7617%5D%7e152%5B83011%5D&page=13"
    chrome = playwrigth.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    page.wait_for_selector("div.category-grid__item")

    html_content = page.content()
    soup = BeautifulSoup(html_content, "html.parser")

    # cards = soup.find_all("div", class_="category-grid__item")

    # for card in cards:
    #     link = card.find("a", class_="product-item product-brick")
    #     if link:
    #         print(link["href"])

    # find view more button is real?
    # see_more = soup.find("div", class_="category-grid__item last-brick")
    see_more = soup.find("span", string="see more")
    if see_more:
        print(see_more.text)
    else:
        print("nixya")

    browser.close()


# vue-product-list-wrap > div.products-list-wrap__products > div.category-grid.category-grid--small-items > div:nth-child(2)
# //*[@id="vue-product-list-wrap"]/div[2]/div[5]/div[2]
# /html/body/div[1]/section[2]/div[1]/div[5]/div/div[2]/div[5]/div[2]

with sync_playwright() as pw:
    get_links(pw)
