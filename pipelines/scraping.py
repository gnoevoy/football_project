from prefect import task, flow
from prefect.logging import get_run_logger
from pathlib import Path
import sys

base_path = Path.cwd() / "web-scraping"
sys.path.append(str(base_path))

from scripts.get_links import get_links
from scripts.get_data import get_data
from scripts.clean_and_load import clean_and_load

params = {"retries": 2, "retry_delay_seconds": 10}


@task(name="scrape_links", **params)
def scrape_links():
    logger = get_run_logger()
    flag = get_links(logger)
    return flag


@task(name="empty_links_file")
def empty_links_file():
    pass


@task(name="scrape_data", **params)
def scrape_data():
    logger = get_run_logger()
    get_data(logger)


@task(name="transform_and_upload", **params)
def transform_and_upload():
    logger = get_run_logger()
    clean_and_load(logger)


@flow(name="web_scraping", **params)
def main():
    is_empty = scrape_links()
    if is_empty:
        empty_links_file()
    else:
        scrape_data()
        # transform_and_upload()


if __name__ == "__main__":
    main()
