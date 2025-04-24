from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from pathlib import Path
import time
import pytz

# Import scripts, db engine and logger
from orders_generator.main import orders_generator
from web_scraping.main import web_scraping
from analytics_pipeline.main import analytics_pipeline
from utils.logger import sheduler_logger
from utils.connections import engine


# Create scheduler with configurations
def create_scheduler():
    timezone = pytz.timezone("Europe/Warsaw")
    # Combine all missed jobs into one and execute it if scheduled time is within the last 5 days
    job_defaults = {"coalesce": True, "max_instances": 1, "misfire_grace_time": 432000}
    executors = {"default": ThreadPoolExecutor(5)}
    jobstores = {"postgres": SQLAlchemyJobStore(engine=engine, tableschema="public", tablename="scheduler")}
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=timezone)
    return scheduler


def main():
    try:
        # Set up logger
        LOGS_DIR = Path(__file__).parent / "logs" / "scheduler"
        logger = sheduler_logger(LOGS_DIR)

        # Start scheduler
        scheduler = create_scheduler()
        scheduler.start()

        # Jobs
        scheduler.add_job(orders_generator, trigger="cron", hour=10, minute=0, id="orders_generator", replace_existing=True, jobstore="postgres")
        scheduler.add_job(web_scraping, trigger="cron", day="*/3", hour=10, minute=5, id="web_scraping", replace_existing=True, jobstore="postgres")
        scheduler.add_job(
            analytics_pipeline, trigger="cron", day="*/3", hour=10, minute=10, id="analytics_pipeline", replace_existing=True, jobstore="postgres"
        )

        # Get next run time for each job
        for job in scheduler.get_jobs():
            logger.info(job)

        # Infinite loop to run scheduler
        while True:
            time.sleep(1)
    except:
        logger.error("", exc_info=True)
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    main()
