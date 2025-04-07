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


def get_region_with_city():
    region = random.choice(list(cities.keys()))
    city = random.choice(cities[region])
    return city, region


def generate_order(order_id):
    city, region = get_region_with_city()
    order = {
        "order_id": order_id,
        "customer_id": random.randint(1, 1000),
        "order_date": fake.date_time_this_year(),
        "payment_method": random.choices(["Bank Transfers", "BLIK", "Credit Card", "Digital Wallet"], weights=[35, 30, 20, 15], k=1)[0],
        "region": region,
        "city": city,
    }
    return order


def generate_order_detail(order_id, products, product):
    order_detail = {
        "order_id": order_id,
        "product_id": product,
        "quantity": random.choices([1, 2], weights=[80, 20], k=1)[0],
        "current_price": products[product]["price"],
        "old_price": products[product]["old_price"],
    }
    order_detail["subtotal"] = round(float(order_detail["current_price"]) * order_detail["quantity"], 2)
    return order_detail
