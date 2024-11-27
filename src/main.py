from static_files import *
from textnode import *


def main():
    my_node = TextNode("This is my text", TextType.BOLD, "https://example.com")
    print(my_node)
    source_path = generate_static_files_list("static/")
    copy_static_to_public(source_path, "public/")

main()