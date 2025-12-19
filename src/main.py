from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
import shutil
import os
import sys
def main():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_files_recursive("static", "docs")
    generate_pages_recursive(dir_path_content="content/", template_path="template.html", dest_dir_path="docs/", basepath=basepath)
if __name__ == "__main__":
    main()