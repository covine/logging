import logging

from .event import Event
from .logger import Logger


logger_dict = dict()


def get_logger(name=None) -> Logger:
    if name:
        if name not in logger_dict.keys():
            logger_dict[name] = Logger(logging.getLogger(name))
        return logger_dict[name]
    else:
        if "root" not in logger_dict.keys():
            logger_dict["root"] = Logger(logging.getLogger())
        return logger_dict["root"]