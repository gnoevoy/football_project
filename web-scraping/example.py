# whisky scraping

from playwright.sync_api import sync_playwright, Playwright
import json


def run(playwrigth: Playwright):
    url = "https://www.thewhiskyexchange.com/c/33/american-whiskey"
    chrome = playwright.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    while True:

        # loop through cards
        cards = page.locator("a[class='product-card js-product-view js-product-click']")
        count = cards.count()

        for i in range(count):
            if i < 1:
                p = browser.new_page(base_url="https://www.thewhiskyexchange.com/")
                url = cards.nth(i).get_attribute("href")

                if url:
                    p.goto(url)
                else:
                    p.close()

                # scrape content on product page
                data = p.locator("script[type='application/ld+json']").text_content()
                json_data = json.loads(data)
                print(json_data["name"])

                p.close()

        # # handle pagination
        current = page.locator(
            "span[class='paging-count__value.js-paging-count__value--end']"
        ).inner_text()
        total = page.locator(
            "span[class='paging-count__value.js-paging-count__value--total']"
        ).inner_text()

        if int(current) == int(total):
            print("no more pages")
            break
        else:
            page.locator(
                ".paging__button.paging__button--next.js-paging__button--loadmore.cta-button.cta-button--regular.js-paging__button.cta-button--bravo"
            ).click()

    browser.close()


with sync_playwright() as playwright:
    run(playwright)
