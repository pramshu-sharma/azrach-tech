import logging
import os
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = os.getenv('LOG_FILE')
LOG_LEVEL = os.getenv('LOG_LEVEL')


def get_logger(name):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'a').close()

    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

