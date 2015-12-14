import unittest
import summarizer


class DataDriver(object):
    def __init__(self):
        self.path = "../data"

class TestSummarizer(unittest.TestCase):
    def setUp(self):
        self.driver = DataDriver()

    def test_txtFinder(self):
        text_gen = summarizer.recursiveFinder(self.driver.path, ".txt")
        filelist = [i for i in text_gen]
        assert len(filelist) == 6260
