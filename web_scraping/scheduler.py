from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
import logging
from pathlib import Path
import time
import pytz
import sys
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_SCHEDULER_STARTED
from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN

from main import main as web_scraping
from utils.connections import engine

my_timezone = pytz.timezone("Europe/Warsaw")
job_defaults = {"coalesce": True, "max_instances": 1}
executors = {"default": ThreadPoolExecutor(5)}
jobstores = {"postgres": SQLAlchemyJobStore(engine=engine, tableschema="public")}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=my_timezone,
)


def simple_func():
    print(f"hello, {datetime.timestamp}")


def my_listener(event):
    # start and shotdown of scheduler
    if event.code == EVENT_SCHEDULER_STARTED:
        print("Scheduler started")
    elif event.code == EVENT_SCHEDULER_SHUTDOWN:
        print("Scheduler shutdown")


scheduler.add_listener(my_listener, EVENT_SCHEDULER_STARTED | EVENT_SCHEDULER_SHUTDOWN)

# Add pipelines to the scheduler
scheduler.add_job(simple_func, "interval", seconds=10, id="simple_func", replace_existing=True, jobstore="postgres")
scheduler.add_job(web_scraping, "cron", minute="*/3", id="web_scraping_job", replace_existing=True, jobstore="postgres")
scheduler.pause_job("web_scraping_job")
scheduler.start()

# Run scheduler
try:
    while True:
        pass
except:
    scheduler.shutdown()
