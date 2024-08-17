import unittest

from src.page_generator import extract_title


class TestPageGenerator(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title"
        self.assertEqual("Title", extract_title(markdown))
    def test_extract_title1(self):
        markdown = "Home is Home\n\n# Title"
        self.assertEqual("Title", extract_title(markdown))
