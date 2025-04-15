from pathlib import Path
import time

# import scripts
from scripts.extract_data import extract_data
from scripts.transform_data import transform_data
from functions.logger import setup_logger

# create log file
LOGS_DIR = Path(__file__).parent / "logs"
logger = setup_logger(LOGS_DIR, "logs")


def main(logger):
    t1 = time.perf_counter()

    # main logic
    # extract_data(logger)
    transform_data(logger)

    t2 = time.perf_counter()
    logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")


if __name__ == "__main__":
    main(logger)
