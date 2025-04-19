from datetime import datetime
import logging


def setup_logger(dir, logger_name):
    # Createa a file name with timestamp
    timestamp = datetime.now().strftime("%m-%d_%H:%M:%S")
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

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
