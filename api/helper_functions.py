from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from collections import defaultdict
from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).parent.parent
sys.path.append(str(PROJECT_DIR))

from utils.connections import engine, mongo_collection


# Tables mapping for using ORM
Base = automap_base()
Base.prepare(autoload_with=engine)
Products = Base.classes.products
Categories = Base.classes.categories
Colors = Base.classes.colors
Labels = Base.classes.labels
Sizes = Base.classes.sizes
Orders = Base.classes.orders
OrderDetails = Base.classes.order_details


# Create a session with automaticall close
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def display_products(db, category_name):
    dct = {}

    # get category data
    category_id = db.query(Categories.category_id).filter(Categories.category_name == category_name).scalar()
    products = db.query(Products).filter(Products.category_id == category_id)
    product_ids = [product.product_id for product in products.all()]

    # add geral info
    total_num = products.count()
    info = {"category_name": category_name, "total_num": total_num}
    dct["info"] = info

    # colors lst
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

    # labels lst
    labels = db.query(Labels).filter(Labels.product_id.in_(product_ids))
    labels_dct = defaultdict(list)
    for label in labels:
        labels_dct[label.product_id].append(label.label)

    # combine all data together witn product features from mongo db
    products_lst = []
    for product in products:
        data = {}
        data["product_id"] = product.product_id
        data["created_at"] = product.created_at
        data["title"] = product.title
        data["price"] = product.price
        data["old_price"] = product.old_price
        data["description"] = product.description
        data["avg_vote_rate"] = product.avg_vote_rate
        data["num_votes"] = product.num_votes

        # define product color
        data["product_color"] = product.title.split("-")[-1].strip()

        # add list of lables the same product models with different colors
        data["related_products"] = colors_dct[product.product_id]
        data["labels"] = labels_dct[product.product_id]

        # get product featues from mongo db
        features = mongo_collection.find_one({"product_id": str(product.product_id)}, {"_id": 0, "product_id": 0})
        data["features"] = features

        products_lst.append(data)
    dct["products"] = products_lst
    return dct


def display_orders(db):
    lst = []

    # retrieve tables from db
    orders = db.query(Orders)
    order_details = db.query(OrderDetails)

    # list of order details
    details = defaultdict(list)
    for detail in order_details:
        row = detail.__dict__
        order_id = row["order_id"]
        row.pop("order_id")
        row.pop("_sa_instance_state", None)
        details[order_id].append(row)

    # unpack order values and add to list
    for order in orders:
        data = order.__dict__
        data.pop("_sa_instance_state", None)

        # add featues to order dct
        id = data["order_id"]
        data["order_details"] = details[id]

        lst.append(data)

    return lst
