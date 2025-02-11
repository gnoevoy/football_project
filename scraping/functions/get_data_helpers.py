from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd


def export_to_csv(data, raw_data_path, file_name):
    df = pd.DataFrame(data)
    df.to_csv(raw_data_path / file_name, index=False, sep=";")


def render_product_page(page):
    """Render and return the main content of the product page."""

    main_content = page.locator("div.main-content-wrap")
    main_content.wait_for()

    # Expand additional sections on the page
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
    avg_vote_rate = content.find(
        "div", class_="tm-grade-label__text tm-score-platforms"
    )
    num_votes = content.find("div", class_="tm-grade-label__text tm-score-platforms")

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
        "avg_vote_rate": avg_vote_rate.text if avg_vote_rate else None,
        "num_votes": num_votes.get("data-reviews") if num_votes else None,
    }
    return product


# For scraping additional product data, the following logic is used in each function:
# 1. Try to extract elements and values – If an element is missing or an error occurs, log the issue.
# 2. Return scraped data – Append it to a list or dictionary for further processing.
# 3. Use success flags – Each function returns a flag to track whether the data was fully scraped.


def get_product_colors(content, product_id, url, logger):
    """Extract and return all available colors for the product."""

    product_colors, flag = [], True
    try:
        colors = content.find(
            "ul",
            class_="model-group-products__wrap model-group-products__wrap--expandable",
        )
        product_colors = []

        for color in colors.find_all("a", class_="model-group-products__link"):
            try:
                color_name = color["href"].split("-")[-1]
                product_color = {"product_id": product_id, "color": color_name}
                product_colors.append(product_color)
            except Exception:
                flag = False
                logger.warning(
                    f"Product {product_id} failed to extract a color - {url}",
                    exc_info=True,
                )

    except Exception:  # Some products dont have colors -> not show error
        return product_colors, flag
    return product_colors, flag


def get_product_labels(content, product_id, url, logger):
    """Extract and return all available labels for the product."""

    product_labels, flag = [], True
    try:
        labels = content.find("div", class_="product-card__badges")

        for label in labels.find_all("span"):
            try:
                product_label = {"product_id": product_id, "label": label.text}
                product_labels.append(product_label)
            except Exception:
                flag = False
                logger.warning(
                    f"Product {product_id} failed to extract a label - {url}",
                    exc_info=True,
                )

    except Exception:
        flag = False
        logger.error(
            f"Product {product_id} failed to get labels element - {url}", exc_info=True
        )
    return product_labels, flag


def get_product_sizes(content, product_id, url, logger):
    """Extract and return all available sizes for the product."""

    product_sizes, flag = [], True
    try:
        sizes = content.find_all(
            "li", class_="nav-item product-attributes__attribute-value"
        )

        for size in sizes:
            try:
                size_num = size.find("span").text
                in_stock = 0 if size.find("button", {"class": "crossed"}) else 1
                product_size = {
                    "product_id": product_id,
                    "size": size_num,
                    "in_stock": in_stock,
                }
                product_sizes.append(product_size)
            except Exception:
                flag = False
                logger.warning(
                    f"Product {product_id} failed to extract a size - {url} ",
                    exc_info=True,
                )

    except Exception:
        flag = False
        logger.error(
            f"Product {product_id} failed to get sizes element - {url}", exc_info=True
        )
    return product_sizes, flag


def get_product_features(content, product_id, url, logger):
    """Extract and return product features from the features table."""

    features, flag = {}, True
    try:
        table = content.find(
            "table",
            class_="product-description-feature",
        )

        for row in table.find_all("tr"):
            try:
                feature = row.find("span", class_="product-description-feature__title")
                value = row.find("span", class_="product-description-feature__value")
                features[feature.text] = value.text
            except Exception:
                flag = False
                logger.warning(
                    f"Product {product_id} failed to extract a feature - {url}",
                    exc_info=True,
                )

    except Exception:
        flag = False
        logger.error(
            f"Product {product_id} failed to get features table - {url}", exc_info=True
        )
    return features, flag


def get_product_images(content, product_id, img_dir, category_folder, url, logger):
    """Download and save all product images to the specified folder."""

    flag = True
    try:
        images = content.find("div", class_="VueCarousel-inner")
        image_num = 1

        for image in images.find_all("img"):
            try:
                link = image["src"]
                data = requests.get(link).content
                image_path = img_dir / category_folder / f"{product_id}-{image_num}.jpg"

                with open(image_path, "wb") as f:
                    f.write(data)
                image_num += 1

            except Exception:
                flag = False
                logger.warning(
                    f"Product {product_id} failed to download an image - {url}",
                    exc_info=True,
                )

    except Exception:
        flag = False
        logger.error(
            f"Product {product_id} doesnt find images element - {url}", exc_info=True
        )
    return flag


if __name__ == "__main__":
    ...
