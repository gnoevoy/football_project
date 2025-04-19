from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime
from pathlib import Path
import time
import pytz
import sys

# Add python path and load variables
# ROOT_DIR = Path(__file__).parents[1]
# sys.path.insert(0, str(ROOT_DIR))

web_scraping_path = Path(__file__).parent / "web_scraping"
# sys.path.insert(0, str(web_scraping_path))
sys.path.append(str(web_scraping_path))

# print(sys.path)

# Import scripts for scheduling
from web_scraping.main import main as web_scraping

raise KeyboardInterrupt

# import scripts
# create a connection to db
# explore db and job list


my_timezone = pytz.timezone("Europe/Warsaw")
job_defaults = {"coalesce": True, "max_instances": 1}
jobstores = {"postgres": SQLAlchemyJobStore()}

scheduler = BackgroundScheduler(job_defaults=job_defaults, jobstores=jobstores, timezone=my_timezone)


# Add pipelines to the scheduler
scheduler.add_job(rite_to_file, "interval", seconds=10)

scheduler.start()


# Run scheduler
try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
