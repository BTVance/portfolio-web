from textnode import TextType, TextNode
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            temp_split_nodes = []
            if len(parts) % 2 == 0:
                raise Exception("Invalid Markdown Syntax")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                       temp_split_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    temp_split_nodes.append(TextNode(part, text_type))
            new_nodes.extend(temp_split_nodes)
    return new_nodes
def extract_markdown_images(text):
    regex = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return regex

def extract_markdown_links(text):
    regex = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return regex