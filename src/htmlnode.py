class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("nyi")
    
    def props_to_html(self):
        props_string = ""
        if self.props != None and isinstance(self.props, dict):
            
            for prop in self.props:
                props_string = props_string + " " + prop + '="' + self.props[prop] + '"'

        return props_string

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
        def __init__(self, tag, value, props=None):
            super().__init__(tag, value, None, props)
        def to_html(self):  
            if self.value == None:
                raise ValueError("All leaf nodes must have a value")      
            if self.tag == None or self.tag == "":
                return self.value
            
            props_string = self.props_to_html()
            return f'<{self.tag}{props_string}>{self.value}</{self.tag}>'
