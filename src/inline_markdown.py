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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        for alt, url in images:
            sections = text.split(f"![{alt}]({url})", 1)
            before = sections[0]
            after = sections[1]

            if before != "":
                new_nodes.append(TextNode(before,TextType.TEXT))
            
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            text = after

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        for alt, url in links:
            sections = text.split(f"[{alt}]({url})", 1)
            before = sections[0]
            after = sections[1]

            if before != "":
                new_nodes.append(TextNode(before,TextType.TEXT))
            
            new_nodes.append(TextNode(alt, TextType.LINK, url))

            text = after

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes