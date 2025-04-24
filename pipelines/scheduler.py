from pathlib import Path
import time

# Import scripts and logger
from orders_generator.main import orders_generator
from web_scraping.main import web_scraping
from analytics_pipeline.main import analytics_pipeline
from utils.scheduler_helpers import create_scheduler, sheduler_logger

# add scheduelr set up in function
# place scheduler logger to logger file (try not to screw up )


def run_scheduler():
    try:
        # Set up logger
        LOGS_DIR = Path(__file__).parent / "logs" / "scheduler"
        logger = sheduler_logger(LOGS_DIR)

        # Start scheduler
        scheduler = create_scheduler()
        scheduler.start()

        # Jobs
        # scheduler.add_job(orders_generator, trigger="cron", hour=10, minute=0, id="orders_generator", replace_existing=True, jobstore="postgres")
        # scheduler.add_job(web_scraping, trigger="cron", day="*/3", hour=10, minute=5, id="web_scraping", replace_existing=True, jobstore="postgres")
        # scheduler.add_job(
        #     analytics_pipeline, trigger="cron", day="*/3", hour=10, minute=10, id="analytics_pipeline", replace_existing=True, jobstore="postgres"
        # )

        # scheduler.add_job(orders_generator, trigger="cron", minute="*/2", id="orders_generator", replace_existing=True, jobstore="postgres")
        scheduler.add_job(web_scraping, trigger="cron", minute="*/2", id="web_scraping", replace_existing=True, jobstore="postgres")
        # scheduler.add_job(analytics_pipeline, trigger="cron", minute="*/2", id="analytics_pipeline", replace_existing=True, jobstore="postgres")

        scheduler.pause_job("orders_generator")
        scheduler.pause_job("analytics_pipeline")

        # Get next run time for each job
        for job in scheduler.get_jobs():
            logger.info(job)

        # Infinite loop to run scheduler
        while True:
            time.sleep(1)
    except:
        logger.error("", exc_info=True)
        scheduler.shutdown()


if __name__ == "__main__":
    run_scheduler()
