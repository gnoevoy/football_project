from bs4 import BeautifulSoup


# Helper functions to get html content once per product page
def render_product_page(page):
    main_content = page.locator("div.main-content-wrap")
    main_content.wait_for()

    # Expand additional sections on the page
    page.locator("a[aria-controls='long-description-desktop']").click()
    page.locator("a[aria-controls='info-text']").click()

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="main-content-wrap")
    return content


# Retrieve core product data, if this function fails the product will be skipped
def get_product(content, url, product_id, category_id):
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

    # Construct dct for item
    product = {
        "product_id": product_id,
        "category_id": category_id,
        "scraped_id": scraped_id,
        "url": url,
        "title": title,
        "price": price,
        "old_price": old_price.text if old_price else None,
        "description": description.find("span").get_text(strip=True) if description else None,
        "avg_vote_rate": avg_vote_rate.text if avg_vote_rate else None,
        "num_votes": num_votes.get("data-reviews") if num_votes else None,
    }
    return product


# Eeach function below is responsible for different content on the product page
# All code has error handling so if something goes wrong it will output problems to logger about this item


def get_sizes(content, url, product_id, logger):
    product_sizes = []
    sizes = content.find_all("li", class_="nav-item product-attributes__attribute-value")

    # Check if object exists
    if sizes:
        # Loop over list of elements and try to extract data
        for size in sizes:
            try:
                size_num = size.find("span").text
                in_stock = False if size.find("button", {"class": "crossed"}) else True
                product_size = {"product_id": product_id, "size": size_num, "in_stock": in_stock}
                product_sizes.append(product_size)
            except:
                logger.error(f"Failed to extract a size, {url}", exc_info=True)
    else:
        logger.error(f"Cannot access sizes, {url}", exc_info=True)
    return product_sizes


def get_labels(content, url, logger):
    product_labels = []
    labels = content.find("div", class_="product-card__badges")

    if labels:
        for label in labels.find_all("span"):
            try:
                product_labels.append(label.text)
            except:
                logger.error(f"Failed to extract a label, {url}", exc_info=True)
    else:
        logger.error(f"Cannot access labels element, {url}", exc_info=True)
    return product_labels


def get_related_products(content, url, logger):
    product_colors = []
    related_products = content.find("ul", class_="model-group-products__wrap model-group-products__wrap--expandable")
    flag = True

    # Not every product has related products, if so construct a message to log it with the help of flag
    if related_products:
        for color in related_products.find_all("a", class_="model-group-products__link"):
            try:
                color_name = color["href"].split("-")[-1]
                product_colors.append(color_name)
            except:
                logger.error(f"Failed to extract a color, {url}", exc_info=True)
    else:
        flag = False

    return product_colors, flag


def get_features(content, url, logger):
    product_features = {}
    table = content.find("table", class_="product-description-feature")

    if table:
        for row in table.find_all("tr"):
            try:
                feature = row.find("span", class_="product-description-feature__title")
                value = row.find("span", class_="product-description-feature__value")
                product_features[feature.text] = value.text
            except:
                logger.error(f"Failed to extract a feature, {url}", exc_info=True)
    else:
        logger.error(f"Cannot access features table, {url}", exc_info=True)
    return product_features


# The decision is to store core data and sizes in postgres tables and additional data in mongo (json format)
# Composing different additional data into one dict
def get_details(content, url, product_id, logger):
    labels = get_labels(content, url, logger)
    related_products, flag = get_related_products(content, url, logger)
    features = get_features(content, url, logger)

    details = {"product_id": product_id, "labels": labels, "related_products": related_products, "features": features}
    return details, flag
