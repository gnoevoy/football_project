from playwright.sync_api import expect
from bs4 import BeautifulSoup


def handle_cookies(page):
    """Handle the cookie consent pop-up."""

    cookie = page.locator("div.CybotCookiebotDialogActive")
    cookie.wait_for()
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")


def get_total_items(page):
    """Retrieve the total number of items from the catalog."""

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    total_items = soup.find(
        "p", class_="products-list-controls-container__paragraph amount"
    )
    return int(total_items.text)


def get_product_links(page, page_num):
    """Extract product links from the current catalog page."""

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    # Get product cards, excluding the "load more" button
    grid = soup.find("div", class_="category-grid category-grid--small-items")
    products = grid.select("div.category-grid__item:not(.last-brick)")

    # Collect links from the product cards
    links = [product.find("a")["href"] for product in products]
    print(f"page: {page_num}  |  links: {len(links)}")
    return links


if __name__ == "__main__":
    ...
