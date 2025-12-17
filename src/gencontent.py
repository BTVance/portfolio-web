from inline_markdown import markdown_to_html_node
import os
def extract_title(markdown):
    new_lines = markdown.splitlines()
    for line in new_lines:
        first_line = line
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            return title
    raise Exception("No h1 header")
def generate_page(from_path, template_path, dest_path):
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

    dir_path = os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(page)


