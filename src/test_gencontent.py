import unittest
from gencontent import extract_title
class TestGenNode(unittest.TestCase):
    def test_extract_title_correct(self):
        node = "# Hello"
        result = extract_title(node)
        expected = "Hello"
        self.assertEqual(result, expected)
    def test_extract_title_empty(self):
        node = ""
        with self.assertRaises(Exception):
            extract_title(node)
    def test_extract_title_wspace(self):
        node = "# Hello "
        result = extract_title(node)
        expected = "Hello"
        self.assertEqual(result, expected)