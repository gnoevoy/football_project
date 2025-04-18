from dotenv import load_dotenv
from pathlib import Path
import requests
import time
import sys
import os

# Add path path and load variables
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

# Import helper functions
from functions.utils import load_file_to_bucket

API_BASE_URL = os.getenv("API_BASE_URL")
api_endpoints = ["boots", "balls", "orders"]


# Get token for auth
def get_token():
    metadata = {"username": os.getenv("API_USER_NAME"), "password": os.getenv("API_USER_PASSWORD")}
    url = f"{API_BASE_URL}/token"
    response = requests.post(url, data=metadata)
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token


# Reach endpoint and get json
def get_data(token, endpoint):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/{endpoint}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data


def extract_data(logger):
    try:
        t1 = time.perf_counter()
        logger.info("EXTRACTING DATA FROM API ...")

        # Get token, reach endpoints and load files to bucket
        token = get_token()
        raw_files_dir = "api-pipeline/raw"

        for endpoint in api_endpoints:
            data = get_data(token, endpoint)
            load_file_to_bucket(data, raw_files_dir, f"{endpoint}.json", file_type="json")
            logger.info(f"{endpoint.title()} successfully extracted and loaded to bucket")

        # Log extraction time
        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")
        logger.info("----------------------------------------------------------------")
    except:
        logger.error(f"", exc_info=True)
