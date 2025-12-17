from textnode import TextNode
from textnode import TextType
from copystatic import copy_recursive
from gencontent import generate_page
import shutil
import os
def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_recursive("static", "public")
    generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html")
if __name__ == "__main__":
    main()