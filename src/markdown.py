from htmlnode import *
from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            pieces = node.text.split(delimiter)
            if len(pieces) %2 == 0:
                raise ValueError("No matching delimiter")
            for i in range(len(pieces)):
                piece = pieces[i]
                if (i == 0 and len(piece) == 0):
                    continue
                
                if i % 2 == 0: 
    # Only skip if it's the first piece (i==0) AND it's empty
                    if not (i == 0 and len(piece) == 0):
                        result.append(TextNode(piece, TextType.TEXT))

                else:
                    if piece == piece.lstrip() and piece == piece.rstrip():
                        result.append(TextNode(piece, text_type))
                    else:
                        original = f"{delimiter}{piece}{delimiter}"
                        result.append(TextNode(original, TextType.TEXT))
        else: 
            result.append(node)
    
    # Debug prints moved here, outside both loops
    return result
def extract_markdown_images(text):
    
    all_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    images_list = [match for match in all_matches if match[1]]
    return images_list
    
def extract_markdown_links(text):

    all_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    links_list = [match for match in all_matches if match[1]]
    return links_list

def extract_markdown_bolds(text):

    all_matches = re.findall(r"\*\*([^\*]+)\*\*", text)
    return all_matches

def extract_markdown_italics(text):
    all_matches = re.findall(r"(\*[^*]+\*)|(_[^_]+_)", text)
    italics_nodes = [
        TextNode(m.strip("*_"), TextType.ITALIC)
        for match in all_matches
        for m in match if m  # Check that m is not an empty string
    ]
    return italics_nodes

def extract_markdown_codes(text):
    all_matches = re.findall(r"`([^`]+)`", text)
    code_nodes = [
        TextNode(m, TextType.CODE)
        for m in all_matches if m  # Check that m is not an empty string
    ]
    return code_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})")
            if len(sections) != 2:
                raise ValueError("image tag not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})")
            if len(sections) != 2:
                raise ValueError("link tag not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):

    if text == "":
        return []

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    new_blocks = []
    temp_block = ""

    for line in markdown.splitlines():
        if line.strip():
            # Accumulate lines with newline or space
            temp_block += line.strip() + "\n"
        else:
            if temp_block.strip():
                new_blocks.append(temp_block.strip())
            temp_block = ""

    # Add the last block if there's any remaining content
    if temp_block.strip():
        new_blocks.append(temp_block.strip())

    return new_blocks

