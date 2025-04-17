from pathlib import Path
import time

# Import scripts
from scripts.extract_data import extract_data
from scripts.transform_data import transform_data
from scripts.load_data import load_data
from functions.logger import setup_logger

# Create log file
LOGS_DIR = Path(__file__).parent / "logs"
logger = setup_logger(LOGS_DIR, "logs")


def main(logger):
    t1 = time.perf_counter()

    # ETL logic
    extract_data(logger)
    new_products, new_orders = transform_data(logger)
    load_data(new_products, new_orders, logger)

    # Log execution time of entire pipeline
    t2 = time.perf_counter()
    logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")


if __name__ == "__main__":
    main(logger)
