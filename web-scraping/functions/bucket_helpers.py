from dotenv import load_dotenv
from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor
import requests
import pandas as pd
import json
import os

load_dotenv(".credentials")

# gcs connection
bucket_name = os.getenv("BUCKET_NAME")
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
web_scraping_path = "web-scraping/data/"


def load_json_links_to_gcs(dct):
    content = json.dumps(dct, indent=4)
    destination = f"{web_scraping_path}scraped_links.json"
    blob = bucket.blob(destination)
    blob.upload_from_string(content, content_type="application/json")


def get_scraped_links_from_gcs():
    blob = bucket.blob(f"{web_scraping_path}scraped_links.json")
    data = json.loads(blob.download_as_string(client=None))
    return data


def load_file_to_gcs(data, file_name, csv=True):
    destination = f"{web_scraping_path}raw/{file_name}"
    blob = bucket.blob(destination)

    if csv:
        df = pd.DataFrame(data)
        blob.upload_from_string(df.to_csv(index=False), content_type="text/csv")
    else:
        content = json.dumps(data, indent=4)
        blob.upload_from_string(content, content_type="application/json")


def load_img_to_gcs(link, img_name):
    content = requests.get(link).content
    destination = f"{web_scraping_path}img/{img_name}"
    blob = bucket.blob(destination)
    blob.upload_from_string(content, content_type="image/jpeg")


def open_file_from_gcs(file_name, csv=True):
    if csv:
        path = f"gs://{bucket_name}/{web_scraping_path}raw/{file_name}"
        df = pd.read_csv(path)
        return df
    else:
        blob = bucket.blob(f"{web_scraping_path}raw/{file_name}")
        data = json.loads(blob.download_as_string(client=None))
        return data


def move_image_in_gcs():
    categories = ["boots", "balls"]
    num = 0

    # helper func to move and delete single blob
    def move_and_delete_blob(blob):
        blob_name = "/".join(blob.name.split("/")[3:])
        destination = f"product-images/{blob_name}"
        bucket.copy_blob(blob, bucket, destination)
        bucket.delete_blob(blob.name)

    # retrieve all files from folder
    for category in categories:
        prefix = f"{web_scraping_path}img/{category}/"
        blobs = [blob for blob in bucket.list_blobs(prefix=prefix) if blob.name.endswith(".jpg")]
        num += len(blobs)

        # parallel execution of moving and deleting blobs
        with ThreadPoolExecutor(max_workers=10) as exec:
            exec.map(move_and_delete_blob, blobs)

    return num
