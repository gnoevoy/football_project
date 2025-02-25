import logging
from logging.handlers import RotatingFileHandler


def setup_logger(file_name):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=file_name,
    )
    logger = logging.getLogger()
    return logger
