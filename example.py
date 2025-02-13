from prefect import flow


@flow
def counter():
    for i in range(3):
        print("hello bars1k")


counter()
