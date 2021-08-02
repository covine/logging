import logging
import unittest

from .. import get_logger


class TestLevel(unittest.TestCase):

    def test_event_level(self):
        logger = get_logger("event_level")
        info_event = logger.info()
        debug_event = logger.debug()
        warn_event = logger.warn()
        error_event = logger.error()
        fatal_event = logger.fatal()
        self.assertEqual(info_event.level, logging.INFO)
        self.assertEqual(debug_event.level, logging.DEBUG)
        self.assertEqual(warn_event.level, logging.WARN)
        self.assertEqual(error_event.level, logging.ERROR)
        self.assertEqual(fatal_event.level, logging.FATAL)

    def test_event_tag(self):
        l = get_logger("event_tag")
        i = l.info()

        i.tag({"name":"a","state":"B"})

        self.assertTrue("name" in i.tags)
        self.assertTrue("state" in i.tags)


if __name__ == '__main__':
    unittest.main()
