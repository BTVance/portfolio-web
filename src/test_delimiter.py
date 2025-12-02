from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
import unittest

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        delimiter = "`"
        text_type = TextType.CODE
        
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        
        result_nodes = split_nodes_delimiter([node], delimiter, text_type)
        
        self.assertEqual(len(result_nodes), len(expected_nodes))
        for i in range(len(result_nodes)):
            self.assertEqual(result_nodes[i], expected_nodes[i])    
    def test_invalid_markdown_delimiter(self):
        node = TextNode("This is text with a `unmatched delimiter", TextType.TEXT)
        delimiter = "`"
        text_type = TextType.CODE

        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], delimiter, text_type)

        self.assertEqual(str(cm.exception), "Invalid Markdown Syntax")
    
    def test_split_multiple_delimit_phrases(self):
        node = TextNode("This has `code1` and `code2` blocks.", TextType.TEXT)
        delimiter = "`"
        text_type = TextType.CODE

        expected_nodes = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks.", TextType.TEXT),
        ]

        result_nodes = split_nodes_delimiter([node], delimiter, text_type)

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for i in range(len(result_nodes)):
            self.assertEqual(result_nodes[i], expected_nodes[i])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [link](https://.bootdev.com)"
    )
        self.assertListEqual([("link", "https://.bootdev.com")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "this is a text with two links [link](https://.bootdev.com), [link](https://google.com)"
        )
        self.assertListEqual([("link", "https://.bootdev.com"), ("link", "https://google.com")], matches)
    
    def test_no_links(self):
        matches = extract_markdown_links(
            "this is a text with no links"
        )
        self.assertEqual([], matches)