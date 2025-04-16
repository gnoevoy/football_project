from dotenv import load_dotenv
from google.cloud import storage
from google.cloud import bigquery
from pathlib import Path
import pandas as pd
import json
import os

ENV_FILE = Path(__file__).parents[1] / ".env"
load_dotenv(ENV_FILE)

# bucket connection
bucket_name = os.getenv("BUCKET_NAME")
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

# bigquery connection
bigquery_client = bigquery.Client()


# load csv of json file to storage
def load_file_to_bucket(data, dir, file_name, file_type="json"):
    destination = f"{dir}/{file_name}"
    blob = bucket.blob(destination)

    if file_type == "csv":
        blob.upload_from_string(data.to_csv(index=False), content_type="text/csv")
    if file_type == "json":
        content = json.dumps(data, indent=4)
        blob.upload_from_string(content, content_type="application/json")


# open csv or json file
def get_file_from_bucket(dir, file_name, file_type="json"):
    if file_type == "csv":
        path = f"gs://{bucket_name}/{dir}/{file_name}"
        df = pd.read_csv(path)
        return df

    if file_type == "json":
        blob = bucket.blob(f"{dir}/{file_name}")
        data = json.loads(blob.download_as_string())
        return data


# load csv file to bigquery
def load_table_to_bigquery(gcs_url, table_id):
    job_config = bigquery.LoadJobConfig(skip_leading_rows=1, source_format=bigquery.SourceFormat.CSV)
    load_job = bigquery_client.load_table_from_uri(gcs_url, table_id, job_config=job_config)
    load_job.result()
