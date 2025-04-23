from pathlib import Path
import time
import sys

# Add python path
PIPELINES_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PIPELINES_DIR))

# Import scripts
from analytics_pipeline.scripts.extract_data import extract_data
from analytics_pipeline.scripts.transform_data import transform_data
from analytics_pipeline.scripts.load_data import load_data
from utils.logger import setup_logger


def analytics_pipeline():
    try:
        # Set up logger
        LOGS_DIR = PIPELINES_DIR / "logs" / "analytics_pipeline"
        logger = setup_logger(LOGS_DIR, "analytics_pipeline")
        t1 = time.perf_counter()

        # ETL logic
        extract_data(logger)
        new_products, new_orders = transform_data(logger)
        load_data(new_products, new_orders, logger)

        # Log execution time of entire pipeline
        t2 = time.perf_counter()
        logger.info(f"Script {Path(__file__).name} finished in {round(t2 - t1, 2)} seconds.")

    except:
        logger.error(f"", exc_info=True)
        raise


if __name__ == "__main__":
    analytics_pipeline()
