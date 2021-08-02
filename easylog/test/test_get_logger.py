import unittest

from .. import get_logger


class TestGetLogger(unittest.TestCase):

    def test_get_root_logger(self):
        self.assertIsNotNone(get_logger())
        self.assertEqual(get_logger(), get_logger('root'))
        self.assertEqual(get_logger('root'), get_logger('root'))

    def test_get_user_define_logger(self):
        self.assertIsNotNone(get_logger('test'))
        self.assertEqual(get_logger('test'), get_logger('test'))


if __name__ == "__main__":
    unittest.main()
