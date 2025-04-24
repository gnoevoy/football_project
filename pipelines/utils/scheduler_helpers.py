from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import logging
import pytz
import sys

# Add python path to import connection
PIPELINES_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PIPELINES_DIR))
from utils.connections import engine

# Set my timezone
timezone = pytz.timezone("Europe/Warsaw")


def create_scheduler():
    # Configurations
    job_defaults = {"coalesce": True, "max_instances": 1}
    executors = {"default": ThreadPoolExecutor(5)}
    jobstores = {"postgres": SQLAlchemyJobStore(engine=engine, tableschema="public", tablename="scheduler")}
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=timezone)
    return scheduler


def sheduler_logger(logs_dir):
    timestamp = datetime.now(timezone).strftime("%m-%d_%H:%M:%S")
    file_name = f"{logs_dir}/logs_{timestamp}.log"
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d_%H:%M:%S")

    # Write logs to a file with specific format
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)

    # Set up a logger
    logger = logging.getLogger("apscheduler")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger
