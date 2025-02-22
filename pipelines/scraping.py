from prefect import task, flow
from pathlib import Path
import sys


@task
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
    scrape_links()
    scrape_data()
    clean_and_load_to_db()
