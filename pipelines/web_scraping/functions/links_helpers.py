from playwright.sync_api import expect
from bs4 import BeautifulSoup


# Launch browser with image blocking
def open_catalog(playwrigth, url):
    browser = playwrigth.chromium.launch(headless=True)
    page = browser.new_page()
    page.route("**/*.{webp,png,jpeg,jpg}", lambda route: route.abort())
    page.goto(url)
    return page, browser


# Handle cookie pop up and ensure it is closed
def handle_cookies(page):
    cookie = page.locator("div.CybotCookiebotDialogActive")
    cookie.wait_for()
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    expect(cookie).to_be_hidden()


# Extract the total number of items in the category from the page
def get_total_items(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    total_items = soup.find("p", class_="products-list-controls-container__paragraph amount")
    return int(total_items.text)


# Scrape product links from the page
def get_links(page, data, logger):
    # Render html
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.category-grid__item:not(.last-brick)")
    scraped_num = 0
    lst = []

    for i, item in enumerate(items, start=1):
        try:
            url = item.find("a")["href"]
            product_id = int(url.split("-")[-1])
            # Add URL to the list if the product is not already scraped (not in db)
            if product_id not in data:
                lst.append(url)
                scraped_num += 1
        except:
            logger.error(f"Failed to extract url {i}, content: {item}", exc_info=True)
    return lst, len(items), scraped_num
