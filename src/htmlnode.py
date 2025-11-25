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
    