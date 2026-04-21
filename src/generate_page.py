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

    filled_template = template.replace("{{ Title }}", title)
    filled_template = filled_template.replace("{{ Content }}", html_content)
    filled_template = filled_template.replace('href="/', 'href="' + base_path)
    filled_template = filled_template.replace('src="/', 'src="' + base_path)
    dir = os.path.dirname(dest_path)
    if dir:
        os.makedirs(dir, exist_ok=True)  # exist_ok=True evita erro se já existir

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(filled_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, base_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, base_path)
