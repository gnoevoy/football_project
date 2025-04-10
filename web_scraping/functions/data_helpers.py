from bs4 import BeautifulSoup


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


# scrape core data for item, no error handling (this data essential)
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


### 1. each functions is responsible for different content on the product page
### 2. all code has error handling and output problems to logger
### 3. flags are needed for logs to check if item was scraped fully or not


def get_sizes(content, url, product_id, logger):
    product_sizes = []
    sizes = content.find_all("li", class_="nav-item product-attributes__attribute-value")
    flag = True

    if sizes:
        for size in sizes:
            try:
                size_num = size.find("span").text
                in_stock = False if size.find("button", {"class": "crossed"}) else True
                product_size = {"product_id": product_id, "size": size_num, "in_stock": in_stock}
                product_sizes.append(product_size)
            except:
                logger.error(f"Failed to extract a size, {url}", exc_info=True)
                flag = False
    else:
        logger.error(f"Cannot access sizes, {url}", exc_info=True)
        flag = False
    return product_sizes, flag


def get_labels(content, url, logger):
    product_labels = []
    labels = content.find("div", class_="product-card__badges")
    flag = True

    if labels:
        for label in labels.find_all("span"):
            try:
                product_labels.append(label.text)
            except:
                logger.error(f"Failed to extract a label, {url}", exc_info=True)
                flag = False
    else:
        logger.error(f"Cannot access labels element, {url}", exc_info=True)
        flag = False
    return product_labels, flag


def get_related_products(content, url, logger):
    product_colors = []
    related_products = content.find("ul", class_="model-group-products__wrap model-group-products__wrap--expandable")
    flag = True
    message = None

    if related_products:
        for color in related_products.find_all("a", class_="model-group-products__link"):
            try:
                color_name = color["href"].split("-")[-1]
                product_colors.append(color_name)
            except:
                logger.error(f"Failed to extract a color, {url}", exc_info=True)
                flag = False
    else:
        message = "no related products"

    return product_colors, flag, message


def get_features(content, url, logger):
    product_features = {}
    table = content.find("table", class_="product-description-feature")
    flag = True

    if table:
        for row in table.find_all("tr"):
            try:
                feature = row.find("span", class_="product-description-feature__title")
                value = row.find("span", class_="product-description-feature__value")
                product_features[feature.text] = value.text
            except:
                logger.error(f"Failed to extract a feature, {url}", exc_info=True)
                flag = False
    else:
        logger.error(f"Cannot access features table, {url}", exc_info=True)
        flag = False
    return product_features, flag


# compose different data into one dct for storing in a mongo db
def get_details(content, url, product_id, logger):
    labels, labels_flag = get_labels(content, url, logger)
    related_products, related_products_flag, message = get_related_products(content, url, logger)
    features, features_flag = get_features(content, url, logger)

    details = {"product_id": product_id, "labels": labels, "related_products": related_products, "features": features}
    return details, labels_flag, related_products_flag, features_flag, message
