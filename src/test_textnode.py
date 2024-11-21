import unittest

from textnode import TextNode, TextType
from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2) 
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertEqual(node, node2)               
    def test_url2(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)   
    def test_text_node_to_html_node_text(self):
        text_to_type = "This is a simple text node"
        text_node = TextNode(text_to_type, TextType.TEXT, None)
        html_node = text_node.text_node_to_html_node()

        self.assertIsNone(html_node.tag)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, text_to_type)
    def test_text_node_to_html_node_exceptions(self):
        text_node = TextNode("This is my other text node", 'TextType.WRONG', None)
        
        # Use self.assertRaises within a context manager
        with self.assertRaises(Exception) as context:
            text_node.text_node_to_html_node()
        
        # Optional: check the exception message
        self.assertEqual(str(context.exception), "Invalid text type")
    
    def test_text_node_to_html_node_bold_text(self):
        text_node = TextNode("make this BOLD", TextType.BOLD, None)
        html_node = text_node.text_node_to_html_node()

        self.assertEqual(html_node.to_html(), "<b>make this BOLD</b>")
    
    def test_text_node_to_html_node_links(self):
        text_node = TextNode("this is a link", TextType.LINK, "https://google.com")
        html_node = text_node.text_node_to_html_node()

        self.assertEqual(html_node.to_html(),'<a href="https://google.com">this is a link</a>')
    
    def test_text_node_to_html_node_images(self):
        text_node = TextNode("alt text for an image", TextType.IMAGE, "https://i.imgur.com/zhfCcCc.jpeg")
        html_node = text_node.text_node_to_html_node()

        self.assertEqual(html_node.to_html(), '<img src="https://i.imgur.com/zhfCcCc.jpeg" alt="alt text for an image" />')

if __name__ == "__main__":
    unittest.main()