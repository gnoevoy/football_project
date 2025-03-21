from helpers.db_connections import engine, mongo_collection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from collections import defaultdict


# Map existing database tables to ORM classes
Base = automap_base()
Base.prepare(autoload_with=engine)
Products = Base.classes.products
Categories = Base.classes.categories
Colors = Base.classes.colors
Labels = Base.classes.labels
Sizes = Base.classes.sizes
Orders = Base.classes.orders
OrderDetails = Base.classes.order_details


# Create a db session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


# Returns all products for a given category
def display_products(db, category_name):
    dct = {}
    category_id = db.query(Categories.category_id).filter(Categories.category_name == category_name).scalar()
    products = db.query(Products).filter(Products.category_id == category_id)
    product_ids = [product.product_id for product in products.all()]

    # Add general category info
    total_num = products.count()
    info = {"category_name": category_name, "total_num": total_num}
    dct["info"] = info

    # Related product colors
    colors = (
        db.query(Colors.product_id, Colors.color, Products.product_id.label("related_product"))
        .filter(Colors.product_id.in_(product_ids))
        .outerjoin(Products, Colors.color == Products.scraped_id)
    )
    colors_dct = defaultdict(list)
    for color in colors:
        # check if product exists
        if color.related_product:
            colors_dct[color.product_id].append(color.related_product)

    # Fetch labels for all products
    labels = db.query(Labels).filter(Labels.product_id.in_(product_ids))
    labels_dct = defaultdict(list)
    for label in labels:
        labels_dct[label.product_id].append(label.label)

    # Fetch sizes and stock availability
    sizes = db.query(Sizes).filter(Sizes.product_id.in_(product_ids))
    sizes_dct = defaultdict(list)
    for size in sizes:
        row = {"size": size.size, "in_stock": size.in_stock}
        sizes_dct[size.product_id].append(row)

    # Final product list
    products_lst = []
    for product in products:
        data = product.__dict__
        data.pop("_sa_instance_state")
        data.pop("scraped_id")
        data.pop("url")
        data.pop("category_id")

        # Extract color from title
        data["product_color"] = product.title.split("-")[-1].strip()

        # Add related products, labels and sizes
        data["related_products"] = colors_dct[product.product_id]
        data["labels"] = labels_dct[product.product_id]
        data["sizes"] = sizes_dct[product.product_id]

        # Fetch additional product features from MongoDB
        features = mongo_collection.find_one({"product_id": str(product.product_id)}, {"_id": 0, "product_id": 0})
        data["features"] = features

        products_lst.append(data)
    dct["products"] = products_lst
    return dct


# Returns all orders and their related order details
def display_orders(db):
    lst = []
    orders = db.query(Orders)
    order_details = db.query(OrderDetails)

    # Group order details by order_id
    details = defaultdict(list)
    for detail in order_details:
        row = detail.__dict__
        order_id = row["order_id"]
        row.pop("order_id")
        row.pop("_sa_instance_state")
        details[order_id].append(row)

    # Combine orders with their related details
    for order in orders:
        data = order.__dict__
        data.pop("_sa_instance_state")

        # add featues to order dct
        id = data["order_id"]
        data["order_details"] = details[id]

        lst.append(data)

    return lst
