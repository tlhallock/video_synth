import logging
from datetime import datetime
import os


def get_logger(name: str):
    log_dir = os.environ.get("LOG_DIR", "/app/logs/")    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    filename = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log")
    fileHandler = logging.FileHandler(filename, mode="a")
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : [%(filename)s:%(lineno)s - %(funcName)s()] : %(message)s",
        "%Y-%m-%d %H:%M:%S")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    return logger