from textnode import TextNode
from textnode import TextType
from copystatic import copy_recursive
import shutil
import os
def main():
    text = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text)

    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_recursive("static", "public")
if __name__ == "__main__":
    main()