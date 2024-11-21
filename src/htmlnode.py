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
            props_string = self.props_to_html()
            if self.value == None and self.tag != "img":
                raise ValueError("All leaf nodes must have a value")      
            if self.tag == None or self.tag == "":
                return self.value
            if self.tag == "img":
                if len(props_string) == 0:
                    raise ValueError("The props cannot be empty!")
                return f'<{self.tag}{props_string} />'
            
            
            return f'<{self.tag}{props_string}>{self.value}</{self.tag}>'
class ParentNode(HTMLNode):
    
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("All ParentNodes must have a tag")
        if self.children == None or len(self.children) == 0: 
            raise ValueError("Children cannot be empty")
        props_string = self.props_to_html()
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        html_string = f'<{self.tag}{props_string}>{children_html}</{self.tag}>'
        return html_string
