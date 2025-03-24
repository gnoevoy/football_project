import requests

# extract token

url = "http://localhost:8082/token"
data = {"username": "bars1k", "password": "bars1k"}

post_response = requests.post(url, data=data)
token_data = post_response.json()
token = token_data["access_token"]

print(token)


orders_url = "http://localhost:8082/orders"
headers = {"Authorization": f"Bearer {token}"}

orders_response = requests.get(orders_url, headers=headers)
print(orders_response.status_code)
print(orders_response.json())
