from datetime import datetime
import logging
import pytz


def setup_logger(dir, logger_name):
    # Createa a file name with timestamp
    timezone = pytz.timezone("Europe/Warsaw")
    timestamp = datetime.now(timezone).strftime("%m-%d_%H:%M:%S")
    file_name = f"{dir}/logs_{timestamp}.log"
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s | %(message)s", datefmt="%Y-%m-%d_%H:%M:%S")

    # Set up a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid outputing logs to old files
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set up a handler (file and console)
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger
