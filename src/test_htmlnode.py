import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class  TestHTMLNode(unittest.TestCase):
    def setUp(self):
        # Any reusable setup goes here
        self.sample_value = "Hello, world!"
        self.simple_tag = "p"
        self.simple_props = {"href": "https://www.google.com", "target": "_blank"}    
    def test_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    def test_initialization_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
 
    def test_repr(self):
        node = HTMLNode("p", "Hello", [], {"class": "highlight"})
        expected_repr = "HTMLNode(tag=p, value=Hello, children=[], props={'class': 'highlight'})"
        self.assertEqual(repr(node), expected_repr)

    def test_simple_leaf_node(self):
        node = LeafNode(self.simple_tag, self.sample_value).to_html()
        expected_response = "<p>Hello, world!</p>"
        self.assertEqual(node, expected_response)
    
    def test_leaf_with_props(self):
        node = LeafNode("a", self.sample_value, self.simple_props).to_html()
        expected_response = '<a href="https://www.google.com" target="_blank">Hello, world!</a>'
        self.assertEqual(node, expected_response)
    def test_leaf_node_no_tag_none(self):
        node = LeafNode(None, "This is plain text").to_html()
        expected_response = "This is plain text"
        self.assertEqual(node, expected_response)

    def test_leaf_node_no_tag_empty_string(self):  
        node = LeafNode("", "This is also plain text").to_html()
        expected_response = "This is also plain text"
        self.assertEqual(node, expected_response)
    def test_leaf_node_value_none(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()
    def test_leaf_node_img_generation(self):
        node = LeafNode("img", None, None)
    
        with self.assertRaises(ValueError) as context:
            node.to_html()
        
        # Optional: Verify the exception message
        self.assertEqual(str(context.exception), "The props cannot be empty!")
if __name__ == "__main__":
    unittest.main()