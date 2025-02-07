from bs4 import BeautifulSoup
import requests
from datetime import datetime


def render_product_page(page):
    """Render and return the main content of the product page."""

    main_content = page.locator("div.main-content-wrap")
    main_content.wait_for()
    page.locator("a[aria-controls='long-description-desktop']").click()
    page.locator("a[aria-controls='info-text']").click()
    page.locator("a[aria-controls='opinions-toggler']").click()

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="main-content-wrap")
    return content


def get_product_data(content, url, product_id, category_id):
    """Extract and return product info"""

    title = content.find("h1", class_="product-card__title").text
    price = content.find(
        "span",
        class_="text-nowrap price-wrapper price currency product-card__current-price",
    ).text
    old_price = content.find(
        "span",
        class_="text-nowrap price-wrapper price currency product-card__old-price",
    )
    scraped_id = url.split("-")[-1]
    description = content.find("div", class_="product-params-content")
    num_votes = content.find(
        "div", class_="hydra-grade__reviews-count tm-score-platforms"
    )
    avg_vote_rate = content.find("div", class_="hydra-grade__value")

    product = {
        "product_id": product_id,
        "category_id": category_id,
        "scraped_id": scraped_id,
        "url": url,
        "created_at": datetime.today().strftime("%Y-%m-%d"),
        "title": title,
        "price": price,
        "old_price": old_price.text if old_price else None,
        "description": (
            description.find("span").get_text(strip=True) if content else None
        ),
        "num_votes": num_votes.find("span").get_text(strip=True) if num_votes else None,
        "avg_vote_rate": avg_vote_rate.text if avg_vote_rate else None,
    }
    return product


def get_product_colors(content, product_id):
    """Extract and return all available colors for the product."""

    colors = content.find(
        "ul",
        class_="model-group-products__wrap model-group-products__wrap--expandable",
    )
    if colors:
        product_colors = []
        for color in colors.find_all("a", class_="model-group-products__link"):
            color_name = color["href"].split("-")[-1]
            product_color = {"product_id": product_id, "color": color_name}
            product_colors.append(product_color)

        return product_colors
    return None


def get_product_labels(content, product_id):
    """Extract and return all available labels for the product."""

    labels = content.find("div", class_="product-card__badges")
    if labels:
        product_labels = []
        for label in labels.find_all("span"):
            product_label = {"product_id": product_id, "label": label.text}
            product_labels.append(product_label)

        return product_labels
    return None


def get_product_sizes(content, product_id):
    """Extract and return all available sizes for the product."""

    sizes = content.find_all(
        "li", class_="nav-item product-attributes__attribute-value"
    )
    if sizes:
        product_sizes = []
        for size in sizes:
            size_num = size.find("span").text
            in_stock = 0 if size.find("button", {"class": "crossed"}) else 1
            product_size = {
                "product_id": product_id,
                "size": size_num,
                "in_stock": in_stock,
            }
            product_sizes.append(product_size)

        return product_sizes
    return None
