import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Setting for log files
def logs_setup(file_name):
    logs_dir = Path.cwd() / "web-scraping" / "data" / "logs"
    log_file = logs_dir / file_name

    # If size of file exceeds 5 mb -> reset it
    log_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=0)
    logging.basicConfig(
        handlers=[log_handler],
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %I:%M",
    )
    return logging.getLogger(file_name)
