from prefect import task, flow
from prefect.logging import get_run_logger
from prefect.cache_policies import INPUTS, RUN_ID
from datetime import timedelta
from pathlib import Path
import sys

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir / "web-scraping"))

# from scripts.get_links import get_links
# from scripts.get_data import get_data
# from scripts.clean_and_load import clean_and_load

params = {
    "retries": 2,
    "retry_delay_seconds": 10,
    "persist_result": True,
    "cache_policy": INPUTS + RUN_ID,
    "cache_expiration": timedelta(days=1),
}


@task(name="scrape_links", log_prints=True, **params)
def scrape_links():
    print("hello bars1k - link")
    # logger = get_run_logger()
    # flag = get_links(logger)
    # return flag


@task(name="empty_links_file")
def empty_links_file():
    pass


@task(name="scrape_data", **params)
def scrape_data():
    print("hello bars1k - data")
    # logger = get_run_logger()
    # get_data(logger)


@task(name="transform_and_upload", **params)
def transform_and_upload():
    print("hello bars1k - load")
    # logger = get_run_logger()
    # clean_and_load(logger)


@flow(name="web_scraping", retries=1, retry_delay_seconds=1)
def web_scraping():
    is_empty = scrape_links()
    if is_empty:
        empty_links_file()
    else:
        scrape_data()
        transform_and_upload()


if __name__ == "__main__":
    # local storage
    # source=str(Path.cwd()),
    # entrypoint=f"{Path(__file__).name}:web_scraping",

    web_scraping.from_source(
        source="https://github.com/gnoevoy/football_project.git",
        entrypoint="pipelines/scraping.py:web-scraping",
    ).deploy(
        name="web-scraping",
        work_pool_name="web-scraping-local",
    )
