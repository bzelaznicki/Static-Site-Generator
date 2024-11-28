from markdown import *
import os



def extract_title(markdown):

    lines = markdown.splitlines()
    title = None
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            break
    
    if title is None:
        raise ValueError("No valid h1 header")
    
    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    if os.path.exists(from_path):
        with open(from_path) as file:
            page_text = file.read()
    else:
        raise Exception("from file not found")
    if os.path.exists(template_path):
        with open(template_path) as file:
            html_template = file.read()
    else:
        raise Exception("template file not found")
    

    
    title = extract_title(page_text)
    html_content = markdown_to_html_node(page_text).to_html()

    full_html = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    destination_folder = os.path.dirname(dest_path)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    with open(dest_path, "w") as file:
        file.write(full_html)