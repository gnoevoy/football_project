from datetime import datetime
import logging
import pytz

# My timezone
timezone = pytz.timezone("Europe/Warsaw")


# Logger for pipelines
def setup_logger(dir, logger_name):
    # Createa a file name with timestamp
    timestamp = datetime.now(timezone).strftime("%m-%d_%H:%M:%S")
    file_name = f"{dir}/logs_{timestamp}.log"
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid outputing logs to old files
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set up a handler
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger


# Create a logger that connects to the APScheduler’s internal logger.
def sheduler_logger(dir):
    # Createa a file name with timestamp
    timestamp = datetime.now(timezone).strftime("%m-%d_%H:%M:%S")
    file_name = f"{dir}/logs_{timestamp}.log"
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Create a logger (the most important lines to get logs)
    logger = logging.getLogger("apscheduler")
    logger.propagate = False
    logger.setLevel(logging.INFO)

    # Set up file and console handlers
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
