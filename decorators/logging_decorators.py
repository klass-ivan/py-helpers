import logging
from inspect import getcallargs

__author__ = 'klass'


def create_log_f(name, level):
    logger = logging.getLogger(name)
    return lambda t: logger.log(level, t)


def log_call_using(log_f, fmt_string="{}"):
    def decorated(f):
        def wrapper(*args, **kwargs):
            log_f(fmt_string.format(**getcallargs(f, *args, **kwargs)))
            return f(*args, **kwargs)
        return wrapper
    return decorated


def log_result_using(log_f, fmt_string):
    def decorated(f):
        def wrapper(*args, **kwargs):
            r = f(*args, **kwargs)
            log_f(fmt_string.format(result=r))
            return r
        return wrapper
    return decorated


def log_call(name, level, fmt_string):
    return log_call_using(create_log_f(name, level), fmt_string)


def log_result(name, level, fmt_string="{result}"):
    return log_result_using(create_log_f(name, level), fmt_string)