from pathlib import Path
import pandas as pd
import json
import sys

# add python path
ROOT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT_DIR))

# import connections
from utils.connections import bucket, bucket_name


def load_file_to_bucket(data, dir, file_name, file_type="json"):
    destination = f"{dir}/{file_name}"
    blob = bucket.blob(destination)

    if file_type == "csv":
        blob.upload_from_string(data.to_csv(index=False), content_type="text/csv")
    if file_type == "json":
        content = json.dumps(data, indent=4)
        blob.upload_from_string(content, content_type="application/json")


def get_file_from_bucket(dir, file_name, file_type="json"):
    if file_type == "csv":
        path = f"gs://{bucket_name}/{dir}/{file_name}"
        df = pd.read_csv(path)
        return df

    if file_type == "json":
        blob = bucket.blob(f"{dir}/{file_name}")
        data = json.loads(blob.download_as_string())
        return data
