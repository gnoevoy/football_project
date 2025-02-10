import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


def logs_setup(file_name):
    logs_dir = Path.cwd() / "scraping" / "data" / "logs"
    log_file = logs_dir / file_name

    log_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=0)

    logging.basicConfig(
        handlers=[log_handler],
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )
    logger = logging.getLogger(file_name)
    return logger
