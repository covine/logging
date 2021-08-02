import json
import logging

from .event import Event


logger_dict = dict()


# TODO Topic Logger, Topic Event
# not thread safe
class Logger:
    def __init__(self, logger: logging.Logger):
        assert isinstance(logger, logging.Logger)
        self._logger = logger
        self._level = logger.level
        self._tags = dict()
        self._kvs = dict()
        self.topic = ""

    def set_level(self, level):
        self._logger.setLevel(level)
        self._level = self._logger.level

    def add_handler(self, handler: logging.Handler):
        self._logger.addHandler(handler)

    def is_enabled_level(self, level):
        return level >= self._level

    def set_tags(self, tags: dict):
        self._tags.update(tags)
        return self

    # must be serializable, without check here
    def set_kvs(self, kvs: dict):
        self._kvs.update(kvs)
        return self

    def set_topic(self, topic: str):
        self.topic = topic

    def info(self) -> Event:
        return Event(self, level=logging.INFO)

    def debug(self) -> Event:
        return Event(self, level=logging.DEBUG)

    def warn(self) -> Event:
        return Event(self, level=logging.WARN)

    def error(self) -> Event:
        return Event(self, level=logging.ERROR)

    def fatal(self) -> Event:
        return Event(self, level=logging.FATAL)

    def record(self, event: Event, exc_info=None, stack_info=False):
        # merge
        tags = dict()
        tags.update(self._tags)
        tags.update(event.tags)

        kvs = dict()
        kvs.update({"topic": self.topic})
        if event.get_topic():
            kvs.update({"topic": event.get_topic()})

        kvs["kvs"] = dict()
        kvs["kvs"].update(self._kvs)
        kvs["kvs"].update(event.kvs)
        
        kvs.update({"tags": tags})
        kvs.update({"name": self._logger.name})
        kvs.update({"time": event.time})
        kvs.update({"level": logging.getLevelName(event.level)})
        kvs.update({"filename": event.file_name})
        kvs.update({"funcName": event.func})
        kvs.update({"lineno": event.line})
        kvs.update({"msg": event.message})

        if exc_info:
            kvs.update({"exc_info": str(event.exc_info)})
        if stack_info:
            kvs.update({"stack_info": event.s_info})

        r = json.dumps(kvs)

        if event.level == logging.DEBUG:
            self._logger.debug(r)
        elif event.level == logging.INFO:
            self._logger.info(r)
        elif event.level == logging.WARN:
            self._logger.warning(r)
        elif event.level == logging.ERROR:
            self._logger.error(r)
        elif event.level == logging.FATAL:
            self._logger.fatal(r)
        else:
            return
