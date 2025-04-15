from google.cloud import bigquery


client = bigquery.Client()

gcs = "gs://football_project/api-pipeline/clean/products.csv"
table_id = "global-grammar-449122-b6.football_project.products"


def load_data_to_bigquery(gcs_url, table_id):
    job_config = bigquery.LoadJobConfig(skip_leading_rows=1, source_format=bigquery.SourceFormat.CSV)
    load_job = client.load_table_from_uri(gcs_url, table_id, job_config=job_config)
    load_job.result()


try:
    load_data_to_bigquery(gcs, table_id)
    print("Data loaded successfully.")
except:
    import traceback

    traceback.print_exc()
