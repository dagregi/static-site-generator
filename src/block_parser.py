import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


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
