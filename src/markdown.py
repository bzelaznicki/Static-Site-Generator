from htmlnode import *
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            pieces = node.text.split(delimiter)
            print(f"Delimiter: {delimiter}")
            print(f"Original text: {node.text}")
            print(f"Pieces: {pieces}")
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
    print("Final nodes:")
    for node in result:
        print(f"- {node.text} ({node.text_type})")
    return result