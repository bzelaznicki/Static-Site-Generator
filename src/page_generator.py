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

def generate_md_files_list(source):
    filelist = []
    directory_files = os.listdir(source)

    for file in directory_files:
        full_path = os.path.join(source, file)  # Combine source and file
        if os.path.isdir(full_path):  # Check if it's a directory
            subfolder_files = generate_md_files_list(full_path)
            filelist += subfolder_files
        if file.endswith(".md"):
            filelist.append(full_path)  # Use full_path here as well

    return filelist


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    md_filelist = generate_md_files_list(dir_path_content)

    if os.path.exists(template_path):
            with open(template_path) as file:
                html_template = file.read()
    else:
        raise Exception("template file not found") 
    
    for md_file in md_filelist:
        if os.path.exists(md_file):
            with open(md_file) as file:
                page_text = file.read()
        else:
            raise Exception("source file not found")

        title = extract_title(page_text)
        html_content = markdown_to_html_node(page_text).to_html()
        full_html = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Create relative path by removing base content directory
        relative_path = os.path.relpath(md_file, dir_path_content)
    # Change .md to .html in destination file name
        destination_file = os.path.splitext(relative_path)[0] + ".html"
        # Note: the entire path, not just the directory for creating directory
        destination_full_path = os.path.join(dest_dir_path, destination_file)
    
        destination_folder = os.path.dirname(destination_full_path)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
    
    # Ensure writing to the correct full path
        with open(destination_full_path, "w") as file:
            file.write(full_html)