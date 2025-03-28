import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s | %(asctime)s | %(message)s")

for i in range(5):
    print(i)
    logging.info(f"hello, {i}")
