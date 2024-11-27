import unittest
from textnode import TextNode, TextType
from markdown import *  # adjust import path as needed

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
    
    def test_image_extraction(self):
        text_with_images = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text_with_images)

        self.assertEqual(extracted_images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_link_extraction(self):
        text_with_links = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text_with_links)

        self.assertEqual(extracted_links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_image_extraction_with_empty_links(self):
        text_with_images = ""
        extracted_images = extract_markdown_images(text_with_images)      

        self.assertEqual(extracted_images, []) 
    
    def test_image_incomplete_syntax(self):
        text_with_images = "![alt text]()"
        extracted_images = extract_markdown_images(text_with_images)   

        self.assertEqual(extracted_images, []) 
    def test_links_incomplete_syntax(self):
        text_with_links = "[link text]()"
        extracted_links = extract_markdown_links(text_with_links)   

        self.assertEqual(extracted_links, [])  
    def test_links_there_arent_even_any_links_here(self):
        text_with_links = "This is text without any links - if you return anything other than an empty list you're a noob"
        extracted_links = extract_markdown_links(text_with_links)   

        self.assertEqual(extracted_links, []) 
    """   
    def test_mixed_links_and_images(self):
        text_with_mixed = "Check out this [link with an image ![alt text](http://image.url)](http://link.url) and more text."
    
        extracted_links = extract_markdown_links(text_with_mixed)
        extracted_images = extract_markdown_images(text_with_mixed)
    
    # Ideas for assertions, depending on expected behavior:
        self.assertEqual(extracted_links, [('link with an image ![alt text', 'http://link.url')])
        self.assertEqual(extracted_images, [('alt text', 'http://image.url')]) 
    """               
    def test_no_image(self):
        node = TextNode("Just some text with no image", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node], "Should return original node if no image")

    def test_single_image(self):
        node = TextNode("Text followed by an image ![alt](image_url)", TextType.TEXT)
        expected_result = [
            TextNode("Text followed by an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "image_url")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_result, "Should split single image correctly")

    def test_multiple_images(self):
        node = TextNode("Image1 ![alt1](image_url1) and Image2 ![alt2](image_url2)", TextType.TEXT)
        expected_result = [
            TextNode("Image1 ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "image_url1"),
            TextNode(" and Image2 ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "image_url2")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_result, "Should split multiple images correctly")

    def test_no_link(self):
        node = TextNode("Just some text with no link", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node], "Should return original node if no link")

    def test_single_link(self):
        node = TextNode("Text followed by a link [Boot.dev](https://www.boot.dev)", TextType.TEXT)
        expected_result = [
            TextNode("Text followed by a link ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_result, "Should split single link correctly")

    def test_multiple_links(self):
        node = TextNode("Search engines like [Google](https://www.google.com) and video platforms like [YouTube](https://www.youtube.com) are popular.", TextType.TEXT)
        expected_result = [
            TextNode("Search engines like ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" and video platforms like ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
            TextNode(" are popular.", TextType.TEXT)
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_result, "Should split multiple links correctly")       
    def test_text_with_bold_and_links(self):
        text = "This is **bold** and a [link](https://example.com)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_text_with_image(self):
        text = "Here is an image ![alt text](https://example.com/image.jpg)"
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_plain_text(self):
        text = "Just plain text"
        expected = [
            TextNode("Just plain text", TextType.TEXT),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(actual, expected)
    def test_empty_string(self):
        text = ""
        expected = []
        actual = text_to_textnodes(text)
        self.assertEqual(actual, expected)



class TestMultilineMarkdown(unittest.TestCase):
    def test_multiline_simple_with_heading(self):
        example_1 = """# Welcome to the Jungle

This is a paragraph with some text.
"""
        expected_results = ['# Welcome to the Jungle', 'This is a paragraph with some text.']
        result = markdown_to_blocks(example_1)
        self.assertEqual(result, expected_results) 

    def test_multiline_multiple_blocks_wih_extra_whitespace(self):
        example_1 = """
### Subheading

  Another paragraph with   varied   spaces.

* Item 1
* Item 2

"""
        expected_results = ['### Subheading', 'Another paragraph with   varied   spaces.', '* Item 1\n* Item 2']
        result = markdown_to_blocks(example_1)
        self.assertEqual(result, expected_results) 

    def test_multiline_consecutive_list_items(self):
        example_1 = """- First Item
- Second Item
- Third Item

End of the list.
"""
        expected_results = ['- First Item\n- Second Item\n- Third Item', 'End of the list.']
        result = markdown_to_blocks(example_1)
        self.assertEqual(result, expected_results) 

    def test_multiline_mixed_content(self):
        example_1 = """
This is a paragraph.
  
  * Bullet 1
  * Bullet 2
  

End paragraph.
"""
        expected_results = [
    "This is a paragraph.",
    "* Bullet 1\n* Bullet 2",
    "End paragraph."
]
        result = markdown_to_blocks(example_1)
        self.assertEqual(result, expected_results) 
    def test_single_block(self):
        md = "This is a single block"
        self.assertEqual(markdown_to_blocks(md), ["This is a single block"])

    def test_multiple_blocks(self):
        md = "# Heading\n\nParagraph text\n\n* List item"
        expected = ["# Heading", "Paragraph text", "* List item"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_consecutive_blank_lines(self):
        md = "# Heading\n\n\n\nParagraph text"
        expected = ["# Heading", "Paragraph text"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_leading_trailing_blank_lines(self):
        md = "\n\n# Heading\n\nParagraph text\n\n\n"
        expected = ["# Heading", "Paragraph text"]
        self.assertEqual(markdown_to_blocks(md), expected)
    
    def test_empty_document(self):
        md = ""
        self.assertEqual(markdown_to_blocks(md), []) 

class TestBlockTypes(unittest.TestCase):
    def test_basic_paragraph(self):
        block = "This is a simple paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_heading(self):
        block = "## Second level heading"
        self.assertEqual(block_to_block_type(block), "heading")
    
    def test_invalid_heading(self):
        block = "##No space after hashtags"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_unordered_list(self):
        block = "* First item\n* Second item"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_ordered_list_thats_not_ordered(self):
        block = "1. First item\n3. Second item\n2. Third item"
        self.assertEqual(block_to_block_type(block), "paragraph")
    def test_multiline_quote(self):
        block = "> This is a quote\n> that spans multiple lines\n> and keeps going"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_heading_too_many_spaces(self):
        block = "#       # Too many spaces after hash"
        self.assertEqual(block_to_block_type(block), "heading")
    
    def test_not_quite_a_list(self):
        block = "1. Not a list\nSomething else\n3. More stuff"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_mixed_style_unordered_list(self):
        block = "* First item\n- Mixed markers\n* Third item"
        self.assertEqual(block_to_block_type(block), "unordered_list")
    
    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_code_on_the_same_line(self):
        block = '```print("hello")```'
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_that_looks_like_a_list_but_isnt(self):
        block = "* First item\nplain text line\n* Last item"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_block_with_some_quotes(self):
        block = "> First item\nplain text line\n> Last item"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_heading_with_no_content(self):
        block = "#"
        self.assertEqual(block_to_block_type(block), "paragraph")  # Should be paragraph because # must be followed by a space
    def test_invalid_ordered_list_start(self):
        block = "2. First\n3. Second\n4. Third"
        self.assertEqual(block_to_block_type(block), "paragraph")  # Should be paragraph because ordered lists must start at 1    
    def test_mixed_list_markers(self):
        block = "1. First\n* Second\n3. Third"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_ordered_list_with_spaces(self):
        block = "1. First    \n2.    Second\n3. Third"
        self.assertEqual(block_to_block_type(block), "ordered_list")
    def test_missing_spaces(self):
        block = "1.First\n2.Second\n3.Third"
        self.assertEqual(block_to_block_type(block), "paragraph")

class TestMarkDownConversions(unittest.TestCase):

    def test_simple_paragraph(self):
        markdown = "Hello world"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), "<div><p>Hello world</p></div>")

    def test_more_paragraphs(self):
        markdown = """
# Header

This is a paragraph.

* List item 1
* List item 2
"""
        self.assertEqual(markdown_to_html_node(markdown).to_html(), "<div><h1>Header</h1><p>This is a paragraph.</p><ul><li>List item 1</li><li>List item 2</li></ul></div>")
    
class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_basic_text(self):
        markdown = "This is a simple text."
        expected_blocks = ["This is a simple text."]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_single_code_block(self):
        markdown = "```\ndef func():\n    pass\n```"
        expected_blocks = ["```\ndef func():\n    pass\n```"]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_mixed_content(self):
        markdown = "Paragraph text.\n```\ncode block\n```\nMore text."
        expected_blocks = ["Paragraph text.", "```\ncode block\n```", "More text."]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_single_line_paragraph(self):
        example = "This is a single line paragraph."
        expected = ["This is a single line paragraph."]
        result = markdown_to_blocks(example)
        self.assertEqual(result, expected)

    def test_nested_code_block(self):
        example = (
            "```"
            "def example():"
            '    return "Markdown!"'
            "```"
        )
        expected = [
            "```"
            "def example():"
            '    return "Markdown!"'
            "```"
        ]
        result = markdown_to_blocks(example)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()