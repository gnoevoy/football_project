from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import logging
import time
import pytz


# Import helper functions
from orders_generator.main import orders_generator
from web_scraping.main import web_scraping
from utils.connections import engine


def create_scheduler():
    # Configurations
    timezone = pytz.timezone("Europe/Warsaw")
    job_defaults = {"coalesce": True, "max_instances": 1}
    executors = {"default": ThreadPoolExecutor(5)}
    jobstores = {"postgres": SQLAlchemyJobStore(engine=engine, tableschema="public", tablename="scheduler")}

    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=timezone)
    return scheduler


def run_scheduler():
    try:
        # Set up logger
        LOGS_DIR = Path(__file__).parent / "logs" / "scheduler"
        timestamp = datetime.now().strftime("%m-%d_%H:%M:%S")
        file_name = f"{LOGS_DIR}/logs_{timestamp}.log"

        logger = logging.getLogger("apscheduler")
        logger.propagate = False
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(file_name)
        logger.addHandler(file_handler)

        # Create configurated scheduler and start it
        scheduler = create_scheduler()
        scheduler.start()

        # Get next run time for each job
        for job in scheduler.get_jobs():
            logger.info(job)

        # Jobs
        scheduler.add_job(orders_generator, "cron", minute="*", id="orders_generator", args=[2], replace_existing=True, jobstore="postgres")

        # Infinite loop to run scheduler
        while True:
            time.sleep(1)
    except:
        logger.error("", exc_info=True)
        scheduler.shutdown()


if __name__ == "__main__":
    run_scheduler()
