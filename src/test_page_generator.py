import unittest
from page_generator import *

class TestExtractTitle(unittest.TestCase):

    def test_simple_header(self):

        input = "# Hello, world!"
        expected_result = "Hello, world!"

        processed_title = extract_title(input)

        self.assertEqual(processed_title, expected_result)

    def test_no_title(self):

        input = "Hey, where did my title go?"
        with self.assertRaises(ValueError):
            extract_title(input)
    
    def test_multiple_headers(self):
        input = """
# First Title
Some text here.
## Secondary Header
# Second Title
Another line of text.
"""
        expected_result = "First Title"

        processed_title = extract_title(input)

        self.assertEqual(processed_title, expected_result)

    def test_empty_title(self):
            input = ""
            with self.assertRaises(ValueError):
                extract_title(input)
    def test_header_in_middle(self):
        input = """
This is some introductory text.
Here we continue with more information.

# The Middle Title

Finally, we end with concluding remarks.
"""
        expected_result = "The Middle Title"

        processed_title = extract_title(input)

        self.assertEqual(processed_title, expected_result)

    def test_title_with_leading_spaces(self):
        input = " # This looks like a title, but isn't"
        with self.assertRaises(ValueError):
            extract_title(input)


            
    def test_title_with_whitespace_and_formatting(self):
        input = """
#  **Amazing Title**    
More content here.
"""
        expected_result = "**Amazing Title**"

        processed_title = extract_title(input)

        self.assertEqual(processed_title, expected_result)    

    def test_title_with_lots_of_whitespace(self):
        input = """
#                                                       **Amazing Title**                                                                                                                                        
More content here.
"""
        expected_result = "**Amazing Title**"

        processed_title = extract_title(input)

        self.assertEqual(processed_title, expected_result)  
    def test_generate_page_empty_file(self):
    # Create a temporary empty markdown file
        with open("empty.md", "w") as f:
            f.write("")
    
    # What do you think will happen when we call generate_page?
    generate_page("empty.md", "template.html", "tests.html")
if __name__ == "__main__":
    unittest.main()