from pathlib import Path

from scripts.extract_links import extract_links
from utils.logger import setup_logger

# create log file
LOGS_DIR = Path(__file__).parent / "logs"
logger = setup_logger(LOGS_DIR, "web_scraping")


def main():
    is_empty = extract_links(logger)
    if not is_empty:
        # extract_data()
        # transform_data()
        # load_data()
        pass
    else:
        pass


if __name__ == "__main__":
    main()
