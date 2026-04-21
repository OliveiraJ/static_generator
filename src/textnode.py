import re
from enum import Enum

from htmlnode import HTMLNode
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class MarkdownDelimiters(Enum):
    CODE = "`"
    BOLD = "*"
    ITALIC = "_"
    LINK = "["
    IMAGE = "![["


class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        if text_type in (TextType.LINK, TextType.IMAGE) and url is None:
            raise ValueError(f"url é obrigatória para o tipo {text_type.value}")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if not isinstance(node, TextNode):
            return NotImplemented
        return (
            self.text == node.text
            and self.text_type == node.text_type
            and self.url == node.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            return LeafNode(
                "img",
                text_node.text,
                {"src": text_node.url if text_node.url is not None else ""},
            )
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.LINK:
            return LeafNode(
                "a",
                text_node.text,
                {"href": text_node.url if text_node.url is not None else ""},
            )
        case _:
            raise ValueError("Invalid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_title(md):
    pattern = r"^#\s+(.+)$"
    title = re.search(pattern, md, re.MULTILINE)
    if title is None:
        raise ValueError("invalid markdown, no title found")
    return title.group(1).strip("# ")


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    clean_blocks = []
    for block in blocks:
        clean_blocks.append(block.strip("\n "))

    return clean_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    # Heading: starts with 1-6 '#' followed by a space
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

    # Multiline code block: starts and ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Quote block: every line starts with '>'
    if all(re.match(r"^>.*", line) for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with '- '
    if all(re.match(r"^- .+", line) for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with incrementing number followed by '. '
    def is_ordered_list(lines):
        for i, line in enumerate(lines, start=1):
            if not re.match(rf"^{i}\. .+", line):
                return False
        return True

    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
