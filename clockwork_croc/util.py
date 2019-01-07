import logging
from functools import wraps

def get_logger(name, fmt=None, level=None):
    bascially_config_log()

    logger = logging.getLogger(name)

    if fmt is not None:
        logger.setFormat(fmt, style='{')

    if level is not None:
        logger.setLevel(level)

    return logger


def bascially_config_log():
    logging.basicConfig(
        format='🤖🐊 {name} {message}',
        style='{',
        level=logging.DEBUG
    )

def memoize(f):
    not_set = object()
    memo = not_set

    @wraps(f)
    def wrapper(*args, **kwargs):
        nonlocal memo
        if memo is not_set:
            memo = f(*args, **kwargs)
        return memo

    return wrapper
