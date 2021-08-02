import os
import logging
import unittest

from .. import get_logger


class TestFileHandler(unittest.TestCase):
    def __init__(self, method_name='runTest'):
        logging.basicConfig(level=logging.INFO)

        self.file = './unittest.log'
        self.handler = logging.FileHandler(filename=self.file, encoding="utf-8")
        format = logging.Formatter('%(message)s')
        self.handler.setFormatter(format)

        super().__init__(method_name)

    def tearDown(self) -> None:
        try:
            os.remove(self.file)
        except Exception as e:
            print(e)

    def test_file_handler(self):
        file_logger = get_logger("file")
        file_logger.add_handler(self.handler)
        # the getEffectiveLevel method of logging lib has some problem
        # we must set the level of logger before we use it
        file_logger.set_level("DEBUG")
        file_logger.debug().msg("test_file_handler")
        with open(self.file, 'rt', encoding='utf-8') as f:
            index = 0
            for _ in f:
                index += 1
        self.assertEqual(index, 1)


if __name__ == '__main__':
    unittest.main()
