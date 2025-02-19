from prefect import task, flow
import random
from datetime import datetime, timezone

num = random.randint(1, 2)

# for tasks such options availabele
# retries and retries duration - simple one
# caching and caching duration - save completed task to not rerun when something fails
# concurrency - parallel execution of task inside flow functions (speed up process)


@task(name="get_num")
def get_num():
    for i in range(3):
        x = i * i


@task(name="wrong_value")
def wrong_value():
    pass


@task(name="write_to_file")
def write_to_file():
    with open("file-1.txt", "a") as f:
        f.write(f"{datetime.now(timezone.utc)} - hello bars1k - {num}\n")


@flow(name="demo-flow")
def main():
    get_num()

    if num == 1:
        write_to_file()
    else:
        wrong_value()


if __name__ == "__main__":
    main()
