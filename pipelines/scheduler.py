from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
import time

# Import helper functions
from utils.scheduler_config import create_scheduler, listener


def simple_func():
    print(f"hello, {time.time()}")


def main():
    # Create a scheduler instance with configurations
    scheduler = create_scheduler()
    scheduler.add_listener(listener, EVENT_SCHEDULER_STARTED | EVENT_SCHEDULER_SHUTDOWN | EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)

    scheduler.add_job(
        simple_func,
        "interval",
        seconds=10,
        id="simple_func",
        replace_existing=True,
        jobstore="postgres",
    )

    try:
        scheduler.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()
