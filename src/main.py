import os
import shutil
import sys

# from pathlib import Path
from generate_page import generate_pages_recursive

STATIC = "./static"
PUBLIC = "./docs"
TEMPLATE = "./template.html"
CONTENT = "./content"
DEFAULT_BASE_PATH = "/"


def main():
    base_path = DEFAULT_BASE_PATH
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    sync_folder_recursive(STATIC, PUBLIC)
    generate_pages_recursive(CONTENT, TEMPLATE, PUBLIC, base_path)


def sync_folder_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            sync_folder_recursive(from_path, dest_path)


if __name__ == "__main__":
    main()
