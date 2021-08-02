import os
import io
import sys
import logging
import datetime
import traceback
import collections.abc


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(2)
else:
    def currentframe():
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


def stone():
    pass


_srcfile = os.path.normcase(stone.__code__.co_filename)


class Event:
    def __init__(self, l, level=logging.NOTSET):
        self._l = l
        self.level = level
        self.time = None
        self._topic = ""
        self.kvs = dict()
        self.tags = dict()
        self.message = str()
        self.file_name = "(unknown file)"
        self.line = 0
        self.func = "(unknown function)"
        self.s_info = None
        self.exc_info = None

    def get_topic(self) -> str:
        return self._topic

    def topic(self, topic: str):
        if not self._l.is_enabled_level(self.level):
            return self
        self._topic = topic
        return self

    def tag(self, tags: dict):
        if not self._l.is_enabled_level(self.level):
            return self

        self.tags.update(tags)
        return self

    # must be serializable, without check here
    def kv(self, kvs: dict):
        if not self._l.is_enabled_level(self.level):
            return self

        self.kvs.update(kvs)
        return self

    @staticmethod
    def find_caller(stack_info=False):
        f = currentframe()
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            s_info = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                s_info = sio.getvalue()
                if s_info[-1] == '\n':
                    s_info = s_info[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, s_info)
            break
        return rv

    def format_exception(self, ei):
        sio = io.StringIO()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return s

    def msg(self, *args, exc_info=None, stack_info=False):
        if not self._l.is_enabled_level(self.level):
            return

        s_info = None
        if _srcfile:
            try:
                fn, lno, func, s_info = self.find_caller(stack_info)
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
                self.exc_info = self.format_exception(exc_info)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
                self.exc_info = self.format_exception(exc_info)
            else:
                self.exc_info = exc_info

        else:
            self.exc_info = None

        # caller
        self.file_name = fn
        self.func = func
        self.line = lno
        # stack info
        self.s_info = s_info

        if args:
            _args = args[1:]
            if len(_args) == 1 and isinstance(_args[0], collections.abc.Mapping) and _args[0]:
                _a = _args[0]
            _a = _args

            m = str(args[0])
            if _a:
                m = m % _a
            self.message = m

        self.time = datetime.datetime.utcnow().isoformat()

        self._l.record(self, self.exc_info, stack_info)
