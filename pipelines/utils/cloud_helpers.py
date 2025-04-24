from pathlib import Path
from google.cloud import bigquery
import pandas as pd
import json
import sys

# Add python path
PIPELINES_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PIPELINES_DIR))

# Import connections
from utils.connections import bucket, bucket_name, bigquery_client


# Load csv of json file to storage
def load_file_to_bucket(data, dir, file_name, file_type="json"):
    destination = f"{dir}/{file_name}"
    blob = bucket.blob(destination)

    if file_type == "csv":
        blob.upload_from_string(data.to_csv(index=False), content_type="text/csv")
    if file_type == "json":
        content = json.dumps(data, indent=4)
        blob.upload_from_string(content, content_type="application/json")


# Open csv or json file from bucket
def get_file_from_bucket(dir, file_name, file_type="json"):
    if file_type == "csv":
        path = f"gs://{bucket_name}/{dir}/{file_name}"
        df = pd.read_csv(path)
        return df

    if file_type == "json":
        blob = bucket.blob(f"{dir}/{file_name}")
        data = json.loads(blob.download_as_string())
        return data


# Load csv file from bucket to bigquery
def load_table_to_bigquery(gcs_url, table_id):
    # simple set up for appending new data to existing table
    job_config = bigquery.LoadJobConfig(skip_leading_rows=1, source_format=bigquery.SourceFormat.CSV)
    load_job = bigquery_client.load_table_from_uri(gcs_url, table_id, job_config=job_config)
    load_job.result()
