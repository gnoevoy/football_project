import requests
from dotenv import load_dotenv
from pathlib import Path
import sys
import os


# how bulk load works
# should i chekc if product_id in warehouse if so skip it ???

# parrallel exections of code for endpoints?


# add path and load variables
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

# import helper functions
from functions.gcs_utils import load_file_to_bucket

# where better to store variables???
BASE_URL = os.getenv("API_BASE_URL")
api_endpoints = ["boots", "balls", "orders"]
bucket_dir = "api-pipeline/raw"


def get_token():
    metadata = {"username": os.getenv("API_USER_NAME"), "password": os.getenv("API_USER_PASSWORD")}
    url = f"{BASE_URL}/token"
    response = requests.post(url, data=metadata)
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token


def get_data(token, endpoint):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data


def extract_data():
    token = get_token()

    for endpoint in api_endpoints:
        data = get_data(token, endpoint)
        load_file_to_bucket(data, bucket_dir, f"{endpoint}.json", file_type="json")
