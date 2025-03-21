from google.cloud import storage
from dotenv import load_dotenv
import os

load_dotenv(".credentials")

# gcs connection
bucket_name = os.getenv("BUCKET_NAME")
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
