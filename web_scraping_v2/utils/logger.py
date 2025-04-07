from datetime import datetime
import logging


def setup_logger(dir, name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    file_name = f"{dir}/{name}_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(filename)s | %(message)s",
        datefmt="%Y-%m-%d_%H:%M:%S",
        filename=file_name,
    )

    return logging.getLogger()
