import requests
import pandas as pd
import json
from pathlib import Path
import sys
import io

# Set base path for helper functions
PROJECT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_DIR))

# Import bucket connection
from utils.connections import bucket


def load_links_to_gcs(dct):
    content = json.dumps(dct, indent=4)
    destination = "web-scraping/scraped_links.json"
    blob = bucket.blob(destination)
    blob.upload_from_string(content, content_type="application/json")


def get_links_from_gcs():
    blob = bucket.blob("web-scraping/scraped_links.json")
    data = blob.download_as_string()
    links = json.loads(data)
    return links


def load_img_to_gcs(link, img_name):
    content = requests.get(link).content
    destination = f"web-scraping/img/{img_name}"
    blob = bucket.blob(destination)
    blob.upload_from_string(content, content_type="image/jpeg")


def load_file_to_gcs(data, path, file_name, csv=True):
    destination = f"{path}/{file_name}"
    blob = bucket.blob(destination)

    if csv:
        blob.upload_from_string(data.to_csv(index=False), content_type="text/csv")
    else:
        content = json.dumps(data, indent=4)
        blob.upload_from_string(content, content_type="application/json")


def open_file_from_gcs(path, file_name, csv=True):
    blob = bucket.blob(f"{path}/{file_name}")

    if csv:
        data = blob.download_as_bytes()
        df = pd.read_csv(io.BytesIO(data))
        return df
    else:
        data = json.loads(blob.download_as_string())
        return data


def move_image_gcs():
    categories = ["boots", "balls"]
    num = 0

    for category in categories:
        prefix = f"web-scraping/img/{category}"

        for blob in bucket.list_blobs(prefix=prefix):
            if blob.name.endswith(".jpg"):
                blob_name = "/".join(blob.name.split("/")[3:])
                destination = f"product-images/{category}/{blob_name}"
                bucket.copy_blob(blob, bucket, destination)
                bucket.delete_blob(blob.name)
                num += 1
    return num


# delete blobl if something went wrong while loading to db / storage data
def delete_blobs_from_gcs():
    categories = ["boots", "balls"]

    # retrieve all files from folder
    for category in categories:
        prefix = f"web-scraping/img/{category}"

        for blob in bucket.list_blobs(prefix=prefix):
            if blob.name.endswith(".jpg"):
                bucket.delete_blob(blob.name)
