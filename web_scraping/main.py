from datetime import datetime
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

# Import scrips
from utils.logger import setup_logger
from web_scraping.scripts.get_links import scrape_links
from web_scraping.scripts.get_data import scrape_data
from web_scraping.scripts.clean_and_load import clean_and_load_data
from utils.db_connectios import postgres_check_connection, mongo_check_connection, gcs_check_connection

try:
    # Set up logger for script
    LOGS_DIR = ROOT_DIR / "logs" / "web_scraping"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
    logger = setup_logger(LOGS_DIR / f"scraping_{timestamp}.log")

    # Check db connections
    postgres_check_connection() == True
    mongo_check_connection() == True
    gcs_check_connection() == True
    logger.info("CONNECTIONS SUCCESSFULLY ESTABLISHED")
    logger.info("")

    # Main logic
    is_empty = scrape_links(logger)
    if not is_empty:
        scrape_data(logger)
        clean_and_load_data(logger)
    else:
        logger.info("No new records in web app")

    logger.info("-------------------------------------------------------")

except Exception:
    logger.error(f"Unexpected error", exc_info=True)
    logger.info("-------------------------------------------------------")
