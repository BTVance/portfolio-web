from textnode import TextNode
from textnode import TextType
from copystatic import copy_recursive
from gencontent import generate_pages_recursive
import shutil
import os
def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_recursive("static", "public")
    generate_pages_recursive(dir_path_content="content/", template_path="template.html", dest_dir_path="public/")
if __name__ == "__main__":
    main()