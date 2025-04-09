from pathlib import Path
import time

from scripts.extract_links import extract_links
from scripts.extract_data import extract_data
from utils.logger import setup_logger

# create log file
LOGS_DIR = Path(__file__).parent / "logs"
logger = setup_logger(LOGS_DIR, "web_scraping")


def main():
    t1 = time.perf_counter()
    is_empty = extract_links(logger)
    if not is_empty:
        extract_data(logger)
    #     transform_data()
    #     load_data()
    #     pass
    else:
        logger.info("No new products on the website")
    t2 = time.perf_counter()


if __name__ == "__main__":
    main()
