import logging
from pathlib import Path


def logs_setup(file_name):
    logs_dir = Path.cwd() / "scraping" / "data" / "logs"
    log_file = logs_dir / file_name

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

    return logging.getLogger(file_name)
