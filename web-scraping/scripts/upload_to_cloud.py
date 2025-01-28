from google.cloud.storage import Client, transfer_manager
from pathlib import Path


# Directory where the files to be uploaded are located
source_directory = Path.cwd() / "web-scraping" / "data"
bucket_name = "football_project"


# Recursively find all files
paths = source_directory.rglob("*")
included_dirs = ["cleaned_data", "product_images"]
str_paths = []

# Filter files based on whether they are in the included directories
for path in paths:
    selected_dirs = any([dir in path.parts for dir in included_dirs])
    if path.is_file() and selected_dirs:
        relative_path = str(path.relative_to(source_directory))  # Get relative path
        str_paths.append(relative_path)

print(len(str_paths))


# Function to upload files to Google Cloud Storage
def upload_directory_with_transfer_manager(
    bucket_name, source_directory, str_paths, workers=8
):
    storage_client = Client()
    bucket = storage_client.bucket(bucket_name)

    # Start the upload.
    results = transfer_manager.upload_many_from_filenames(
        bucket, str_paths, source_directory=source_directory, max_workers=workers
    )

    for name, result in zip(str_paths, results):
        if isinstance(result, Exception):
            print(f"Failed to upload {name} due to exception: {result}")
        else:
            print(f"Uploaded {name} to {bucket.name}.")


upload_directory_with_transfer_manager(bucket_name, source_directory, str_paths)
