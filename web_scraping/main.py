from datetime import datetime
from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).parent.parent
sys.path.append(str(PROJECT_DIR))

# Import scrips
from utils.logger import setup_logger
from web_scraping.scripts.get_links import scrape_links
from web_scraping.scripts.get_data import scrape_data
from web_scraping.scripts.clean_data import clean_data
from web_scraping.scripts.load_data import load_data

# Set up logger for script
LOGS_DIR = PROJECT_DIR / "logs" / "web_scraping"
timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
logger = setup_logger(LOGS_DIR / f"scraping_{timestamp}.log")


try:
    # Main logic
    is_empty = scrape_links(logger)
    if is_empty:
        logger.info("No new records in web app")
    else:
        scrape_data(logger)
        clean_data(logger)
        load_data(logger)

    logger.info("-------------------------------------------------------")

except Exception:
    logger.error(f"Unexpected error", exc_info=True)
    logger.info("-------------------------------------------------------")
