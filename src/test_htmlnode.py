import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com", 
             "target": "_blank",
        }
        node = HTMLNode(tag="a", value=None,children=None,props=props)
        result = node.props_to_html()
        expected =  ' href="https://www.google.com" target="_blank"'
        self.assertEqual(result, expected)
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="hello", children=None, props={})
        result = node.props_to_html()
        expected = ""
        self.assertEqual(result, expected)
    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="hello", children=None, props=None)
        result = node.props_to_html()
        expected = ""
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()