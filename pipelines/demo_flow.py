from prefect import flow, task


@task(log_prints=True)
def task1():
    print("hello - task1")


@task(log_prints=True)
def task2():
    print("hello - task2")


@task(log_prints=True)
def task3():
    print("hello - task3")


@flow(name="simple-flow")
def my_flow():
    task1()
    task2()
    task3()


if __name__ == "__main__":
    my_flow()
