from inline_markdown import markdown_to_html_node
from pathlib import Path
import os
def extract_title(markdown):
    new_lines = markdown.splitlines()
    for line in new_lines:
        first_line = line
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            return title
    raise Exception("No h1 header")
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_content = f.read()
    with open(template_path) as f:
        template_content = f.read()
    node = markdown_to_html_node(markdown_content)
    html_string = node.to_html()
    title = extract_title(markdown_content)
    
    page = template_content.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_string)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    dir_path = os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(page)
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    os.makedirs(dest_dir_path, exist_ok=True)
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        to_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path) and from_path.endswith(".md"):
            html_path = Path(to_path).with_suffix(".html")
            generate_page(from_path, template_path, html_path, basepath)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, to_path, basepath)







