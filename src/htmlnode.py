from textnode import TextType
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  
        self.value = value
        self.children = children or []
        self.props = props or {}
    def to_html(self):
        raise [NotImplementedError]
    def props_to_html(self):
        if not self.props:
            return ""
        else:
            string = ""
            for key, value in self.props.items():
                string += f' {key}="{value}"'
            return string
    def __repr__(self):
        return f"tag={self.tag}, value={self.value}, children={self.children}, props={self.props}"
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None,props=props)
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
           attrs = None
           if self.props is None:
                attrs = ""
           else:
                attrs = ""
                for key, value in self.props.items():
                    attrs += f' {key}="{value}"'
        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children,props=props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is missing")
        if not self.children:
            raise ValueError("children missing")
        else:
            attrs = ""
            if self.props:
                attrs = "".join(f' {key}="{value}"' for key, value in self.props.items())

            inner_html = "".join(child.to_html() for child in self.children)

            return f"<{self.tag}{attrs}>{inner_html}</{self.tag}>"
        
def text_node_to_html_node(text_node):
    t = text_node.text
    tt = text_node.text_type

    if tt == TextType.TEXT:
        return LeafNode(None, t)
    elif tt == TextType.BOLD:
        return LeafNode("b", t)
    elif tt == TextType.ITALIC:
        return LeafNode("i", t)
    elif tt == TextType.CODE:
        return LeafNode("code", t)
    elif tt == TextType.LINK:
        if text_node.url is None:
            raise ValueError("Link TextNode must have url")
        return LeafNode("a", t, props={"href": text_node.url})
    elif tt == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("Image TextNode must have url")
        return LeafNode("img", "", props={"src": text_node.url, "alt" : t})
    raise Exception("Invalid TextType for text_node_to_html_node")
        
