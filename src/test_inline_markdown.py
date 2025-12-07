from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
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

    def test_links_with_image(self):
        matches = extract_markdown_links(
            "this is a text with a link and an image [link](https://.bootdev.com), ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("link", "https://.bootdev.com")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://bootdev.com) and another [link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://bootdev.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "link", TextType.LINK, "https://google.com"
            ),
        ],
        new_nodes,
    )
        
    def test_split_images_no_image(self):
        node = TextNode("Just some text", TextType.TEXT)
        result = split_nodes_image([node])
        return result

    def test_split_links_no_link(self):
        node = TextNode("Just some text", TextType.TEXT)
        result = split_nodes_link([node])
        return result
    
    def test_split_images_single_middle(self):
        node = TextNode(
        "start ![alt](http://img.com/p.png) end",
        TextType.TEXT,
    )
        result = split_nodes_image([node])
        return result
    
    def test_split_links_single_middle(self):
        node = TextNode(
        "start [text](http://example.com) end",
        TextType.TEXT,
    )
        result = split_nodes_link([node])
        return result 
    
    def test_split_links_multiple(self):
        node = TextNode(
        "A [one](http://a.com) and [two](http://b.com)",
        TextType.TEXT,
    )
        result = split_nodes_link([node])
        return result
    
    def test_split_images_at_start(self):
        node = TextNode(
        "![alt](http://img.com/p.png) trailing",
        TextType.TEXT,
    )
        result = split_nodes_image([node])
        return result
    
    def test_split_links_at_end(self):
        node = TextNode(
        "leading [text](http://example.com)",
        TextType.TEXT,
    )
        result = split_nodes_link([node])
        return result
    
    def test_split_images_multiple_nodes_input(self):
        nodes = [
        TextNode("First ![one](http://a.com)", TextType.TEXT),
        TextNode("Second ![two](http://b.com)", TextType.TEXT),
    ]
        result = split_nodes_image(nodes)
        return result
    
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual([
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        result)
    def test_text_to_text_nodes_no_markdown(self):
        text = "This is a simple text string"
        result = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is a simple text string", TextType.TEXT),
        ],
        result)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_block_to_blocks_heading(self):
        block = "### Hello There"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, result)

    def test_block_to_blocks_code(self):
        block = "```Yes this is a code block```"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, result)

    def test_block_to_blocks_code(self):
        block = ">Wow\n>Woah\n>What?"
        result = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, result)
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

def test_heading_and_paragraph(self):
    md = """# Title

Some _italic_ text."""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><h1>Title</h1><p>Some <i>italic</i> text.</p></div>",
    )

def test_unordered_list_inline(self):
    md = """- first **bold**
- second _italic_
- third `code`"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><ul><li>first <b>bold</b></li><li>second <i>italic</i></li><li>third <code>code</code></li></ul></div>",
    )

def test_ordered_list_inline(self):
    md = """1. item _one_
2. item **two**
3. item `three`"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><ol><li>item <i>one</i></li><li>item <b>two</b></li><li>item <code>three</code></li></ol></div>",
    )

def test_quote_block(self):
    md = """> This is a _quote_
> with **bold** text"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><blockquote>This is a <i>quote</i>\nwith <b>bold</b> text</blockquote></div>",
    )

def test_mixed_blocks(self):
    md = """# Title

Paragraph here.

- one
- two

1. first
2. second
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><h1>Title</h1><p>Paragraph here.</p><ul><li>one</li><li>two</li></ul><ol><li>first</li><li>second</li></ol></div>",
    )