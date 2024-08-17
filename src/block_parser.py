import re

from inline_parser import text_to_textnode
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_htmlnode(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type_paragraph == block_type:
            nodes.append(paragraph_to_htmlnode(block))
        if block_type_heading == block_type:
            nodes.append(heading_to_htmlnode(block))
        if block_type_code == block_type:
            nodes.append(code_to_htmlnode(block))
        if block_type_quote == block_type:
            nodes.append(quote_to_htmlnode(block))
        if block_type_unordered_list == block_type:
            nodes.append(list_to_htmlnode(block, "ul"))
        if block_type_ordered_list == block_type:
            nodes.append(list_to_htmlnode(block, "ol"))

    return ParentNode("div", nodes)


def markdown_to_blocks(markdown):
    return [
        block.strip() for block in markdown.split("\n\n") if len(block.strip()) != 0
    ]


def block_to_block_type(block):
    if re.search(r"^(#{1,6}\s)", block):
        return block_type_heading
    if re.search(r"^(`{3}.*[\n\r][^]]*?`{3})", block):
        return block_type_code
    if re.search(r"^(>.*)", block):
        return block_type_quote
    if re.search(r"^\d+\.[\S\n\r]*", block):
        return block_type_ordered_list
    if re.search(r"^(\*|-)\s[\S\n\r]*", block):
        return block_type_unordered_list
    else:
        return block_type_paragraph


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnode(text)]


def paragraph_to_htmlnode(block):
    return ParentNode("p", text_to_children(block))


def heading_to_htmlnode(block):
    return ParentNode(
        f"h{len(block.split(' ', 1)[0])}", text_to_children(block.split(" ", 1)[1])
    )


def code_to_htmlnode(block):
    return ParentNode("pre", [LeafNode("code", block.strip("```"))])


def quote_to_htmlnode(block):
    return ParentNode(
        "blockquote",
        text_to_children("\n".join(ln.strip(">") for ln in block.split("\n"))),
    )


def list_to_htmlnode(block, list_type):
    return ParentNode(
        list_type,
        [
            ParentNode("li", text_to_children(ln.split(" ", 1)[1]))
            for ln in block.split("\n")
        ],
    )
