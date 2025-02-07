from playwright.sync_api import expect
from bs4 import BeautifulSoup


def handle_cookies(page):
    cookie = page.locator("div.CybotCookiebotDialogActive")
    cookie.wait_for()
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    expect(cookie).to_be_hidden()


def get_total_items(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    total_items = soup.find(
        "p", class_="products-list-controls-container__paragraph amount"
    )
    return int(total_items.text)


def get_product_links(page, db_data):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    products = soup.select("div.category-grid__item:not(.last-brick)")

    urls = []
    for product in products:
        url = product.find("a")["href"]
        id = int(url.split("-")[-1])
        if id not in db_data:
            urls.append(url)
    return urls


if __name__ == "__main__":
    ...
