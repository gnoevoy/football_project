from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
import pytz

# Import db connection
from utils.connections import engine


def create_scheduler():
    timezone = pytz.timezone("Europe/Warsaw")
    job_defaults = {"coalesce": True, "max_instances": 1}
    executors = {"default": ThreadPoolExecutor(5)}
    jobstores = {"postgres": SQLAlchemyJobStore(engine=engine, tableschema="public")}

    scheduler = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone=timezone,
    )
    return scheduler


def listener(event):
    print(event.scheduled_run_times)
    # print(event.__dict__)

    # # start and shutdown
    # if event.code == EVENT_SCHEDULER_STARTED:
    #     print("Scheduler started")
    # elif event.code == EVENT_SCHEDULER_SHUTDOWN:
    #     print("Scheduler shutdown")

    # # fail and success
    # elif event.code == EVENT_JOB_EXECUTED:
    #     print(f"Job {event.job_id} executed")
    # elif event.code == EVENT_JOB_ERROR:
    #     print(f"Job {event.job_id} error")

    # # missed
    # elif event.code == EVENT_JOB_MISSED:
    #     print(f"Job {event.job_id} missed")
