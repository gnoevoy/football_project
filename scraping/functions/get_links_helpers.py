from playwright.sync_api import expect
from bs4 import BeautifulSoup


def handle_cookies(page):
    """Handles cookie pop-up."""

    cookie = page.locator("div.CybotCookiebotDialogActive")
    cookie.wait_for()
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    expect(cookie).to_be_hidden()  # Ensures the cookie dialog is closed


def get_total_items(page):
    """Extracts the total number of items displayed in the category."""

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    total_items = soup.find( "p", class_="products-list-controls-container__paragraph amount")
    return int(total_items.text) if total_items else None

def get_product_links(page, db_data, logger):
    """Scrapes product links, filtering out already stored products."""

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    products = soup.select("div.category-grid__item:not(.last-brick)")

    urls = []
    for product in products:
        # write error message in log file if some links can't be scraped
        try:
            url = product.find("a")["href"]
            id = int(url.split("-")[-1])
            if id not in db_data:
                urls.append(url)
        except Exception:
            logger.error(f"Failed to extract a url - {url}", exc_info=True)

    return urls


if __name__ == "__main__":
    ...
