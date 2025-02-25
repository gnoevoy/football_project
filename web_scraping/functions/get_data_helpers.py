from bs4 import BeautifulSoup
from datetime import datetime, timezone
from functions.bucket_helpers import load_img_to_gcs  # now sure about this import (cron job)


def render_product_page(page):
    """Render and return the main content of the product page."""

    main_content = page.locator("div.main-content-wrap")
    main_content.wait_for()

    # Expand additional sections on the page
    page.locator("a[aria-controls='long-description-desktop']").click()
    page.locator("a[aria-controls='info-text']").click()

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="main-content-wrap")
    return content


# This function lacks error handling to ensure all content is scraped.
# If an error occurs, the product is skipped.
def get_product_data(content, url, product_id, category_id):
    """Extract and return product info"""

    title = content.find("h1", class_="product-card__title").text
    price = content.find(
        "span",
        class_="text-nowrap price-wrapper price currency product-card__current-price",
    ).text
    old_price = content.find("span", class_="text-nowrap price-wrapper price currency product-card__old-price")
    scraped_id = url.split("-")[-1]
    description = content.find("div", class_="product-params-content")
    avg_vote_rate = content.find("div", class_="tm-grade-label__text tm-score-platforms")
    num_votes = content.find("div", class_="tm-grade-label__text tm-score-platforms")

    product = {
        "product_id": product_id,
        "category_id": category_id,
        "scraped_id": scraped_id,
        "url": url,
        "created_at": datetime.now(timezone.utc),
        "title": title,
        "price": price,
        "old_price": old_price.text if old_price else None,
        "description": (description.find("span").get_text(strip=True) if content else None),
        "avg_vote_rate": avg_vote_rate.text if avg_vote_rate else None,
        "num_votes": num_votes.get("data-reviews") if num_votes else None,
    }
    return product


# The functions below follow a similar logic:
# 1. They attempt to access a specific element, if unsuccessful -> display error.
# 2. If the element is found, they extract individual sub-elements and scrape the required data.
# 3. Each function includes a flag to track whether the scraping process was fully successful.


def get_product_colors(content, product_id, url, logger):
    """Extract and return all available colors for the product."""

    product_colors, flag = [], True
    colors = content.find("ul", class_="model-group-products__wrap model-group-products__wrap--expandable")

    # Some products may not have colors, if missing -> proceed with scraping.
    if colors:
        try:
            for color in colors.find_all("a", class_="model-group-products__link"):
                try:
                    color_name = color["href"].split("-")[-1]
                    product_color = {"product_id": product_id, "color": color_name}
                    product_colors.append(product_color)
                except Exception:
                    flag = False
                    logger.error(f"Failed to extract a color, {url}", exc_info=True)

        except Exception:
            logger.error(f"Cannot access color element, {url}", exc_info=True)
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
                logger.error(f"Failed to extract a label, {url}", exc_info=True)

    except Exception:
        flag = False
        logger.error(f"Cannot access labels element, {url}", exc_info=True)
    return product_labels, flag


def get_product_sizes(content, product_id, url, logger):
    """Extract and return all available sizes for the product."""

    product_sizes, flag = [], True

    try:
        sizes = content.find_all("li", class_="nav-item product-attributes__attribute-value")
        for size in sizes:
            try:
                size_num = size.find("span").text
                in_stock = False if size.find("button", {"class": "crossed"}) else True
                product_size = {"product_id": product_id, "size": size_num, "in_stock": in_stock}
                product_sizes.append(product_size)
            except Exception:
                flag = False
                logger.error(f"Failed to extract a size, {url}", exc_info=True)

    except Exception:
        flag = False
        logger.error(f"Cannot access sizes element, {url}", exc_info=True)
    return product_sizes, flag


def get_product_features(content, url, logger):
    """Extract and return product features from the features table."""

    features, flag = {}, True

    try:
        table = content.find("table", class_="product-description-feature")
        for row in table.find_all("tr"):
            try:
                feature = row.find("span", class_="product-description-feature__title")
                value = row.find("span", class_="product-description-feature__value")
                features[feature.text] = value.text
            except Exception:
                flag = False
                logger.error(f"Failed to extract a feature, {url}", exc_info=True)

    except Exception:
        flag = False
        logger.error(f"Cannot access features table, {url}", exc_info=True)
    return features, flag


def get_product_images(content, product_id, category_folder, url, logger):
    """Load product images to the bucket."""

    flag = True
    images = content.find("div", class_="VueCarousel-inner")
    product_images = []

    try:
        image_num = 1
        for image in images.find_all("img"):
            try:
                link = image["src"]

                # add value to list
                img_name = f"{category_folder}/{product_id}-{image_num}.jpg"
                is_thumbnail = True if image_num == 1 else False
                row = {"product_id": product_id, "image": img_name, "is_thumbnail": is_thumbnail}
                product_images.append(row)

                # upload image to gcs
                load_img_to_gcs(link, img_name)
                image_num += 1

            except Exception:
                flag = False
                logger.error(f"Failed to extract an image, {url}", exc_info=True)

    except Exception:
        flag = False
        logger.error(f"Cannot access images, {url}", exc_info=True)
    return product_images, flag
