import os
import logging
import unittest

from .. import get_logger


class TestFileHandler(unittest.TestCase):
    def __init__(self, method_name='runTest'):
        self.level_file = './level.log'
        self.tag_file = './tag.log'
        self.kv_file = './kv.log'

        logging.basicConfig(level=logging.INFO)

        format = logging.Formatter('%(message)s')

        self.level_handler = logging.FileHandler(filename=self.level_file, encoding="utf-8")
        self.level_handler.setFormatter(format)

        self.tag_handler = logging.FileHandler(filename=self.tag_file, encoding="utf-8")
        self.tag_handler.setFormatter(format)

        self.kv_handler = logging.FileHandler(filename=self.kv_file, encoding="utf-8")
        self.kv_handler.setFormatter(format)

        super().__init__(method_name)

    def test_level(self):
        level_logger = get_logger("test_level")
        level_logger.add_handler(self.level_handler)
        level_logger.set_level("WARN")
        level_logger.set_topic("topicA")

        level_logger.debug().kv({"age": 10, "sex": 1.0}).msg()
        level_logger.debug().tag({"name": "hello"}).kv({"age": 10, "sex": 1.0}).msg()
        level_logger.debug().kv({"age": 11, "sex": 1.0}).msg("my name is %s", "Tom1", exc_info=None, stack_info=True)
        level_logger.info().kv({"age": 12, "sex": 1.0}).msg("my name is %s", "Tom2")
        level_logger.warn().topic("topicB").kv({"age": 13, "sex": 1.0}).msg("my name is %s", "Tom3")
        level_logger.error().kv({"age": 14, "sex": 1.0}).msg("my name is %s", "Tom4")
        level_logger.fatal().kv({"age": 15, "sex": 1.0}).msg("my name is %s", "Tom5")

        with open(self.level_file, 'rt', encoding='utf-8') as f:
            index = 0
            for _ in f:
                index += 1
        self.assertEqual(index, 3)

        try:
            os.remove(self.level_file)
        except Exception as e:
            print(e)

    def test_tag(self):
        tag_logger = get_logger("test_tag")
        tag_logger.add_handler(self.tag_handler)
        tag_logger.set_level("DEBUG")

        tag_logger.set_tags({"name": "L_TAG_1", "state": "L_TAG_2", "task": "TODO"})

        tag_logger.debug().kv({"age": 10, "sex": 1.0}).msg()
        try:
            raise Exception("hello")
        except Exception as e:
            tag_logger.info().kv({"age": 11, "sex": 2.0}).msg("my name is %s", "Tom2", exc_info=e)

        tag_logger.warn().kv({"age": 12, "sex": 3.0}).msg("my name is %s", "Tom3")
        tag_logger.error().tag({"name": "error"}).kv({"age": 13, "sex": 4.0}).msg("my name is %s", "Tom4")
        tag_logger.fatal().tag({"name": "fatal"}).kv({"age": 14, "sex": 5.0}).msg("my name is %s age %d", "Tom5", 100)

        with open(self.tag_file, 'rt', encoding='utf-8') as f:
            index = 0
            for _ in f:
                index += 1
        self.assertEqual(index, 5)

        try:
            os.remove(self.tag_file)
        except Exception as e:
            print(e)

    def test_kv(self):
        kv_logger = get_logger("test_kv")
        kv_logger.add_handler(self.kv_handler)
        kv_logger.set_level("DEBUG")

        kv_logger.set_kvs({"k1": "a", "k2": 1})

        kv_logger.debug().kv({"age": 10, "sex": 1.0}).msg("my name is %s", "Tom1", exc_info=None, stack_info=True)
        kv_logger.info().kv({"age": 11, "sex": 2.0}).msg("my name is %s", "Tom2", exc_info="hello")
        kv_logger.info().kv({"age": 12, "sex": 3.0}).msg("my name is %s", "Tom2")
        kv_logger.warn().kv({"age": 13, "sex": 4.0}).msg("my name is %s", "Tom3")
        kv_logger.error().kv({"age": 14, "sex": 5.0}).msg("my name is %s", "Tom4")
        kv_logger.error().kv({"age": 15, "sex": 6.0}).msg("my name is %s", {"tom4": "hello"})
        kv_logger.error().kv({"age": 16, "sex": 7.0}).msg({"tom4": "hello"})
        kv_logger.fatal().kv({"age": 17, "sex": 8.0}).msg("my name is %s", "Tom5")

        with open(self.kv_file, 'rt', encoding='utf-8') as f:
            index = 0
            for _ in f:
                index += 1
        self.assertEqual(index, 8)

        try:
            os.remove(self.kv_file)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()
