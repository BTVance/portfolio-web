from textnode import TextType, TextNode
from htmlnode import HTMLNode, text_node_to_html_node, ParentNode
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            clean_blocks.append(stripped)
    return clean_blocks

def block_to_block_type(block):
    #Code check
    lines = block.split("\n")
    first_line = lines[0]
    last_line = lines[-1]
    if first_line.startswith("```") and last_line.endswith("```"):
        return BlockType.CODE
    #Heading Check
    num_hashes = 0
    for ch in first_line:
        if ch == "#":
            num_hashes += 1
        else:
            break
    if 1<= num_hashes <= 6 and len(first_line) > num_hashes and first_line[num_hashes] == " ":
        return BlockType.HEADING
    #quote check
    for line in lines:
        if not line.startswith(">"):
            break
    else:
        return BlockType.QUOTE
    #unordered list check
    for line in lines:
        if not line.startswith ("- "):
            break
    else:
        return BlockType.UNORDERED_LIST
    #Ordered list check
    for i, line in enumerate(lines, start=1):
        expected_prefix = f"{i}. "
        if not line.startswith(expected_prefix):
            break
    else:
        return BlockType.ORDERED_LIST
    #normal paragraph
    return BlockType.PARAGRAPH

def text_to_children(text):
    t = text
    text_nodes = text_to_textnodes(t)
    html_nodes = []
    for nodes in text_nodes:
        converted_nodes = text_node_to_html_node(nodes)
        html_nodes.append(converted_nodes)
    return html_nodes

def markdown_to_html_node(markdown):
    #splits markdown into blocks
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        #create html_node based on type
        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            clean_lines = [line.strip() for line in lines if line.strip() != ""]
            joined = " ".join(clean_lines)
            children_text = text_to_children(joined)
            child = ParentNode("p", children_text)
            children.append(child)
        elif block_type == BlockType.HEADING:
            num_hashes = 0
            for ch in block:
                if ch == "#":
                    num_hashes += 1
                else:
                    break
            if 1<= num_hashes <= 6 and len(block) > num_hashes and block[num_hashes] == " ":
                tag = f"h{num_hashes}"
                clean_text = block[num_hashes + 1:].lstrip()
                children_text = text_to_children(clean_text)
                child = ParentNode(tag, children_text)
                children.append(child)
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                if line.startswith(">"):
                    clean_lines.append(line.lstrip(">").lstrip())
                else:
                    clean_lines.append(line)
            clean_text = "\n".join(clean_lines)
            children_text = text_to_children(clean_text)
            child = ParentNode("blockquote", children_text)
            children.append(child)
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                if line.startswith("```"):
                    clean_lines.append(line.lstrip("```").lstrip())
                else:
                    clean_lines.append(line)
            clean_text = "\n".join(clean_lines)
            children_text = TextNode(clean_text, TextType.CODE, url=None)
            child = text_node_to_html_node(children_text)
            pre_node = ParentNode("pre", [child])
            children.append(pre_node)
        elif block_type == BlockType.UNORDERED_LIST:
            ul_children = []
            for line in block.split("\n"):
                item_text = None
                if line.startswith("- "):
                   item_text = line.lstrip("- ").lstrip()
                elif line.startswith("* "):
                    item_text = line.lstrip("* ").lstrip()
                
                if not item_text:
                    continue
                
                children_for_item = text_to_children(item_text)
                li_node = ParentNode("li", children_for_item)
                ul_children.append(li_node)

            ul_node = ParentNode("ul", ul_children)
            children.append(ul_node)
        
        elif block_type == BlockType.ORDERED_LIST:
            ol_children = []
            for line in block.split("\n"):
                line = line.strip()
                if not line:
                    continue
                
                if ". " not in line:
                    continue

                _, item_text = line.split(". ", 1)
                
                children_for_item = text_to_children(item_text)
                li_node = ParentNode("li", children_for_item)
                ol_children.append(li_node)

            ol_node = ParentNode("ol", ol_children)
            children.append(ol_node)    
    return ParentNode("div", children)   

