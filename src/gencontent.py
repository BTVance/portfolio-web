from inline_markdown import markdown_to_blocks
def extract_title(markdown):
    new_lines = markdown.splitlines()
    for line in new_lines:
        first_line = line
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            return title
    raise Exception("No h1 header")
        
