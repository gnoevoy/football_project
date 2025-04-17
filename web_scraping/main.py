from pathlib import Path
import time

# Import scripts
from scripts.extract_links import extract_links
from scripts.extract_data import extract_data
from scripts.transform_data import transform_data
from scripts.load_data import load_data
from utils.logger import setup_logger

# Create log file
LOGS_DIR = Path(__file__).parent / "logs"
logger = setup_logger(LOGS_DIR, "logs")


def main():
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


if __name__ == "__main__":
    main()
