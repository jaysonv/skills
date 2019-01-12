from functools import wraps
import logging
from datetime import datetime


def log_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        result = func(*args, **kwargs)
        logger.info('Result is: {}'.format(result))
        return result
    return wrapper

def make_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string