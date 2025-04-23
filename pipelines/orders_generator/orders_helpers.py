import random
from faker import Faker


fake = Faker("pl_PL")
cities = {
    "Dolnośląskie": ["Wrocław", "Legnica", "Wałbrzych"],
    "Kujawsko-Pomorskie": ["Bydgoszcz", "Toruń", "Włocławek"],
    "Lubelskie": ["Lublin", "Chełm", "Zamość"],
    "Lubuskie": ["Zielona Góra", "Gorzów Wielkopolski"],
    "Łódzkie": ["Łódź", "Piotrków Trybunalski", "Pabianice"],
    "Małopolskie": ["Kraków", "Tarnów", "Nowy Sącz"],
    "Mazowieckie": ["Warszawa", "Radom", "Płock"],
    "Opolskie": ["Opole", "Nysa", "Brzeg"],
    "Podkarpackie": ["Rzeszów", "Przemyśl", "Stalowa Wola"],
    "Podlaskie": ["Białystok", "Łomża", "Suwałki"],
    "Pomorskie": ["Gdańsk", "Gdynia", "Sopot"],
    "Śląskie": ["Katowice", "Gliwice", "Częstochowa"],
    "Świętokrzyskie": ["Kielce", "Ostrowiec Świętokrzyski"],
    "Warmińsko-Mazurskie": ["Olsztyn", "Elbląg", "Ełk"],
    "Wielkopolskie": ["Poznań", "Kalisz", "Konin"],
    "Zachodniopomorskie": ["Szczecin", "Koszalin", "Kołobrzeg"],
}


# Create combination of regions and city for order
def get_region_with_city():
    region = random.choice(list(cities.keys()))
    city = random.choice(cities[region])
    return city, region


# Create an order with given details
def create_order(order_id, quantity, total_price):
    city, region = get_region_with_city()
    order = {
        "order_id": order_id,
        "customer_id": random.randint(1, 1200),
        "order_date": fake.date_time_this_year(),
        "payment_method": random.choices(["Bank Transfers", "BLIK", "Credit Card", "Digital Wallet"], weights=[35, 30, 20, 15], k=1)[0],
        "region": region,
        "city": city,
        "quantity": quantity,
        "total_price": total_price,
    }
    return order


# Create details for a specific product in an order
def create_order_details(order_id, product_id, product_data):
    order_detail = {
        "order_id": order_id,
        "product_id": product_id,
        "quantity": random.choices([1, 2], weights=[90, 10], k=1)[0],
        "current_price": product_data["price"],
        "old_price": product_data["old_price"],
    }
    order_detail["subtotal"] = round(float(order_detail["current_price"]) * order_detail["quantity"], 2)

    # Select a size for the product, giving higher weight to popular sizes
    popular_sizes = ["40", "41", "42", "43", "5"]
    weights = [70 if size in popular_sizes else 30 for size in product_data["sizes"]]
    order_detail["size"] = random.choices(product_data["sizes"], weights=weights, k=1)[0]
    return order_detail


# Generate multiple orders and their details
def generate_orders(orders_num, order_id, products):
    orders, order_details = [], []
    counter = 0

    for _ in range(orders_num):
        products_num = random.randint(1, 2)
        # Select random products for the order
        order_products = random.sample(list(products.keys()), products_num)
        quantity, total_price = 0, 0

        # Create order details for each selected product
        for product in order_products:
            product_data = products[product]
            order_detail = create_order_details(order_id, product, product_data)
            quantity += order_detail["quantity"]
            total_price += order_detail["subtotal"]
            order_details.append(order_detail)
            counter += 1

        # Create the order with aggregated details
        order = create_order(order_id, quantity, total_price)
        orders.append(order)
        order_id += 1

    return orders, order_details, counter
