
from datetime import datetime
from time import time
from uuid import uuid4
from typing import Union


def get_time(seconds_precision=True) -> datetime:
    return datetime.now()
    # return time() if not seconds_precision else int(time())


def create_uuid() -> str:
    return str(uuid4())
