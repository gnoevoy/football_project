from prefect import task, flow
from pathlib import Path


@task(log_prints=True)
def scrape_links():
    print("hello")


@task
def scrape_data():
    print("hello")


@task
def clean_and_load_to_db():
    print("hello")


@flow
def scraping():
    x = scrape_links()
    y = scrape_data()
    z = clean_and_load_to_db()
