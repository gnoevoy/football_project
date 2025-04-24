from pathlib import Path
import time
import sys

# Add python path
PIPELINES_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PIPELINES_DIR))

# Import scripts and logger
from web_scraping.scripts.extract_links import extract_links
from web_scraping.scripts.extract_data import extract_data
from web_scraping.scripts.transform_data import transform_data
from web_scraping.scripts.load_data import load_data
from utils.logger import setup_logger


def web_scraping():
    try:
        # Set up logger
        LOGS_DIR = PIPELINES_DIR / "logs" / "web_scraping"
        logger = setup_logger(LOGS_DIR, "web_scraping")
        t1 = time.perf_counter()

        # Extract links and check if there are new products
        is_empty = extract_links(logger)

        # If new products exist, run the next steps
        if not is_empty:
            extract_data(logger)
            transform_data(logger)
            load_data(logger)
        else:
            logger.info("No new products on the website")
            logger.info("----------------------------------------------------------------")

        # Log execution time
        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")

    except:
        logger.error("", exc_info=True)
        raise


if __name__ == "__main__":
    web_scraping()
