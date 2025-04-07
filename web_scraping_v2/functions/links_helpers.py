from playwright.sync_api import expect
from bs4 import BeautifulSoup


def open_catalog(playwrigth, url):
    # Launch browser with image blocking
    browser = playwrigth.chromium.launch(headless=False)
    page = browser.new_page()
    page.route("**/*.{webp,png,jpeg,jpg}", lambda route: route.abort())
    page.goto(url)
    return page, browser


def handle_cookies(page):
    cookie = page.locator("div.CybotCookiebotDialogActive")
    cookie.wait_for()
    page.click("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    # Ensures the cookie dialog is closed
    expect(cookie).to_be_hidden()


def get_total_items(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    total_items = soup.find("p", class_="products-list-controls-container__paragraph amount")
    return int(total_items.text)


def get_links(page, data, logger):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.category-grid__item:not(.last-brick)")
    num_scraped, num_passed = 0, 0
    lst = []

    for i, item in enumerate(items, start=1):
        try:
            url = item.find("a")["href"]
            product_id = int(url.split("-")[-1])

            # check if the product is already scraped
            if product_id not in data:
                lst.append(url)
                num_scraped += 1
            num_passed += 1

        except Exception:
            logger.error(f"Failed to extract {i} url, content: {item}", exc_info=True)

    return lst, len(items), num_scraped, num_passed
