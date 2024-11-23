import unittest
from textnode import TextNode, TextType
from markdown import split_nodes_delimiter  # adjust import path as needed

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("Hello `world` today", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " today")

    def test_no_delimiters(self):
        node = TextNode("Hello world", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Hello world")

    def test_multiple_delimiter_pairs(self):
        node = TextNode("Hello *world* and *planet*", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "planet")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)

    def test_invalid_delimiter(self):
        node = TextNode("Hello *world", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_non_text_node(self):
        node = TextNode("Hello *world*", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
    def test_mismatched_delimiters(self):
        node = TextNode("Hello *world* extra *stuff", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)
    def test_valid_markdown(self):
        node = TextNode("Hello *world*", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
    def test_multiple_delimiters_with_text(self):
        node = TextNode("Hello *world* middle *stuff* end", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[2].text, " middle ")
        self.assertEqual(nodes[3].text, "stuff")
        self.assertEqual(nodes[4].text, " end")

    def test_delimiter_at_start(self):
        node = TextNode("*world* rest", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        print(nodes)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "world")
        self.assertEqual(nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(nodes[1].text, " rest")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

if __name__ == '__main__':
    unittest.main()