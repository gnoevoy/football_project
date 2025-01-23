from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import re


def render_product_page(page):
    main_content = page.locator("div.main-content-wrap")
    main_content.wait_for()
    page.locator("a[aria-controls='long-description-desktop']").click()
    page.locator("a[aria-controls='info-text']").click()

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="main-content-wrap")
    return content


def get_product_data(content, link, product_id, category_id):
    scraped_id = link.split("-")[-1]
    title = content.find("h1", class_="product-card__title").text
    price = content.find(
        "span",
        class_="text-nowrap price-wrapper price currency product-card__current-price",
    ).text
    description = (
        content.find("div", class_="product-params-content").find("span").contents
    )
    item = {
        "id": product_id,
        "scaped_id": scraped_id,
        "category_id": category_id,
        "name": title,
        "price": price,
        "description": description,
        "link": link,
    }
    return item


def get_product_colors(content, product_id):
    colors = content.find(
        "ul",
        class_="model-group-products__wrap model-group-products__wrap--expandable",
    )
    if colors:
        product_colors = []
        for color in colors.find_all("a", class_="model-group-products__link"):
            color_id = color["href"].split("-")[-1]
            product_color = {"product_id": product_id, "color_id": color_id}
            product_colors.append(product_color)

        return product_colors


def get_product_sizes(content, product_id):
    all_size = content.find(
        "ul",
        class_="product-attributes mb-2",
    )
    product_sizes = []
    for size in all_size.find_all(
        "li", class_="nav-item product-attributes__attribute-value"
    ):
        size_num = size.find("span").text
        in_stock = 0 if size.find("button", {"class": "crossed"}) else 1
        product_size = {
            "product_id": product_id,
            "size_num": size_num,
            "in_stock": in_stock,
        }
        product_sizes.append(product_size)

    return product_sizes


def get_product_features(content, product_id):
    table = content.find(
        "table",
        class_="product-description-feature",
    )
    product_features = {"product_id": product_id}

    for row in table.find_all("tr"):
        feature = row.find("span", class_="product-description-feature__title").text
        value = row.find("span", class_="product-description-feature__value").text
        product_features[feature] = value

    return product_features


if __name__ == "__main__":
    pass
