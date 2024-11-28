from static_files import *
from textnode import *
from page_generator import *


def main():
    my_node = TextNode("This is my text", TextType.BOLD, "https://example.com")
    print(my_node)
    source_path = generate_static_files_list("static/")
    copy_static_to_public(source_path, "public/")

    generate_page("content/index.md", "template.html", "public/index.html")

main()