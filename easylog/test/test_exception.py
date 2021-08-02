import os
import logging
import unittest

from .. import get_logger


class TestExceptionHandler(unittest.TestCase):
    def __init__(self, method_name='runTest'):
        self.exception_file = './exception.log'

        logging.basicConfig(level=logging.INFO)

        format = logging.Formatter('%(message)s')

        self.exception_handler = logging.FileHandler(filename=self.exception_file, encoding="utf-8")
        self.exception_handler.setFormatter(format)

        super().__init__(method_name)

    def test_exception(self):
        self.exception_logger = get_logger("test_exception")
        self.exception_logger.add_handler(self.exception_handler)
        self.exception_logger.set_level("DEBUG")
        self.exception_logger.set_topic("topicA")

        try:
            print('a')
            print('b')
            raise Exception("hello")
        except Exception as e:
            self.exception_logger.error().msg("error: %s", e, exc_info=True)

        try:
            print('a')
            print('b')
            raise Exception("base exception test")
        except BaseException as e:
            self.exception_logger.error().msg("base error: %s", e, exc_info=e)

        try:
            print('a')
            print('b')
            raise Exception("base exception test")
        except BaseException as e:
            self.exception_logger.error().msg("base error: %s", e, exc_info=e.args)

        with open(self.exception_file, 'rt', encoding='utf-8') as f:
            index = 0
            for _ in f:
                index += 1
        self.assertEqual(index, 3)

        try:
            os.remove(self.exception_file)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()