from bs4 import BeautifulSoup
import requests
from datetime import datetime


def render_product_page(page):
    """
    Render and return the main content of the product page.
    Ensures all necessary sections (description, features) are fully loaded.
    """

    main_content = page.locator("div.main-content-wrap")
    main_content.wait_for()
    page.locator("a[aria-controls='long-description-desktop']").click()
    page.locator("a[aria-controls='info-text']").click()

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="main-content-wrap")
    return content


def get_product_data(content, link, product_id, category_id):
    """
    Extract and return basic product information, including ID, name, price,
    description, and link.
    """

    title = content.find("h1", class_="product-card__title").text
    price = content.find(
        "span",
        class_="text-nowrap price-wrapper price currency product-card__current-price",
    ).text
    before_discount = content.find(
        "span",
        class_="text-nowrap price-wrapper price currency product-card__old-price",
    )
    scraped_num = link.split("-")[-1]
    description = (
        content.find("div", class_="product-params-content").find("span").contents
    )
    item = {
        "product_id": product_id,
        "category_id": category_id,
        "name": title,
        "price": price,
        "before_discount": before_discount.text if before_discount else None,
        "description": description,
        "scraped_num": scraped_num,
        "scraped_link": link,
        "created_at": datetime.today().strftime("%Y-%m-%d"),
    }

    return item


def get_product_colors(content, product_id):
    """
    Extract and return all available colors for the product.
    Each color includes the product ID and a unique color ID.
    """

    colors = content.find(
        "ul",
        class_="model-group-products__wrap model-group-products__wrap--expandable",
    )
    if colors:
        product_colors = []
        for color in colors.find_all("a", class_="model-group-products__link"):
            color_name = color["href"].split("-")[-1]
            product_color = {"product_id": product_id, "color_name": color_name}
            product_colors.append(product_color)

        return product_colors

    return None


def get_product_labels(content, product_id):
    labels = content.find("div", class_="product-card__badges")
    if labels:
        product_labels = []
        for label in labels.find_all("span"):
            product_label = {"product_id": product_id, "label_name": label.text}
            product_labels.append(product_label)

        return product_labels

    return None


def get_product_sizes(content, product_id):
    """
    Extract and return all available sizes for the product.
    Each size includes the product ID, size number, and stock availability.
    """

    product_sizes = []
    for size in content.find_all(
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
    """
    Extract and return product features from the features table.
    Each feature includes a title and value, mapped to the product ID.
    """

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


def get_product_images(content, link, product_id, images_folder, category_folder):
    """
    Download and save all product images to the specified folder.
    Images are named using the product ID and an incrementing number.
    """

    images = content.find("div", class_="VueCarousel-inner")
    image_num = 1

    for image in images.find_all("img"):
        link = image["src"]
        data = requests.get(link).content
        image_path = images_folder / category_folder / f"{product_id}-{image_num}.jpg"

        with open(image_path, "wb") as f:
            f.write(data)

        image_num += 1


if __name__ == "__main__":
    pass
