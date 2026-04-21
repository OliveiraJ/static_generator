import os
from pathlib import Path

from markdown_blocks import markdown_to_html_node
from textnode import extract_title


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        content = f.read()

    with open(template_path, "r") as f2:
        template = f2.read()

    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
    template = template.replace('href="/', 'href="' + base_path)
    template = template.replace('src="/', 'src="' + base_path)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, base_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, base_path)
