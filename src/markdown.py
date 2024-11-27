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
    in_code_block = False

    for line in markdown.splitlines():
        if line.startswith('```'):
            if len(temp_block) > 0 and not in_code_block:
                new_blocks.append(temp_block.strip())
                temp_block = ""
            in_code_block = not in_code_block
            # Add the delimiter back into the temp_block
            temp_block += line + "\n"
            # If closing a code block, append the block now
            if not in_code_block:
                new_blocks.append(temp_block.strip())
                temp_block = ""
            continue
        if line.strip() or in_code_block:
    # If not in a code block, trim spaces from the line
            if not in_code_block:
                temp_block += line.strip() + "\n"
            else:
                temp_block += line + "\n"

        else:
            if temp_block.strip():
                new_blocks.append(temp_block.strip())
            temp_block = ""

    # Add the last block if there's any remaining content
    if temp_block.strip():
        new_blocks.append(temp_block.strip())

    return new_blocks

def block_to_block_type(block):
    block_lines = block.splitlines()
    if len(block_lines) > 1 and block_lines[0].startswith("```") and block_lines[-1].startswith("```"):
        return "code"
    
    if block.startswith('#'):
        original_length = len(block)
        stripped = block.lstrip('#')
        hash_count = original_length - len(stripped)

        if hash_count > 0 and hash_count <= 6 and stripped.startswith(" "): 
            return "heading"

    if block.startswith('>'):
        its_a_quote = True
        for line in block_lines:
            if not line.startswith(">"):
                its_a_quote = False
                break
        if its_a_quote:
            return "quote"
        
    
    if block.startswith("* ") or block.startswith("- "):

        its_a_list = True
        for line in block_lines:
            if not line.startswith("* ") and not line.startswith("- "):
                its_a_list = False
                break
        if its_a_list:
            return "unordered_list"

    if len(block_lines) == 0:
        return "paragraph"
    is_ordered_list = True
    for index, line in enumerate(block_lines):
        expected_number = index + 1
    # check if line starts with the expected number followed by ". "
        if not line.startswith(str(expected_number) + ". "):
            is_ordered_list = False
            break

    if is_ordered_list:
        return "ordered_list"
    
    
    
    return "paragraph"

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    converted_nodes = []
    for node in text_nodes:
        converted_nodes.append(node.text_node_to_html_node())
    
    return converted_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])

    for block in blocks:
        blocktype = block_to_block_type(block)
        
        match(blocktype):
            case "paragraph":
                children = text_to_children(block)
                new_node = ParentNode("p", children)
                parent_node.children.append(new_node)
            
            case "heading":
                original_length = len(block)
                stripped = block.lstrip('#')
                hash_count = original_length - len(stripped)
                children = text_to_children(stripped.lstrip())
                new_node = ParentNode(f"h{hash_count}", children)
                parent_node.children.append(new_node)
            
            case "quote":
                stripped = block.lstrip('>')
                stripped = stripped.lstrip()
                children = text_to_children(stripped)
                new_node = ParentNode("blockquote", children)
                parent_node.children.append(new_node)
            
            case "code":
                code_lines = block.splitlines()
                code_content = code_lines[1:-1]
                stripped = "\n".join(code_content)
                code_html = LeafNode(None, stripped)
                code_node = [ParentNode("code", [code_html])]
                pre_node = ParentNode("pre", code_node)
                parent_node.children.append(pre_node)
            
            case "unordered_list":
                lines = block.splitlines()
                li_nodes = []
                for line in lines:
                    converted = text_to_children(line.lstrip("* "))
                    li_nodes.append(ParentNode("li", converted))
                ul_node = ParentNode("ul", li_nodes)
                parent_node.children.append(ul_node)
            
            case "ordered_list":
                lines = block.splitlines()
                li_nodes = []
                for index, line in enumerate(lines):
                    converted = text_to_children(line.lstrip(f"{index + 1}. "))
                    li_nodes.append(ParentNode("li", converted))
                ol_node = ParentNode("ol", li_nodes)
                parent_node.children.append(ol_node)



    
    return parent_node