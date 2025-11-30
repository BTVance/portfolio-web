from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            temp_split_nodes = []
            for i, part in enumerate(parts):
                if len(parts) % 2 == 0:
                    raise Exception("Invalid Markdown Syntax")
                if i % 2 == 1:
                    if i % 2 == 0:
                       temp_split_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    temp_split_nodes.append(TextNode(part, text_type))
            new_nodes.extend(temp_split_nodes)
    return new_nodes