import unittest

from src.block_parser import (
    block_to_block_type,
    markdown_to_blocks,
    block_type_heading,
    block_type_paragraph,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)


class TestBlockParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        document = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        self.assertEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            markdown_to_blocks(document),
        )

    def test_markdown_to_blocks2(self):
        document = """# Heading

## Heading 2

    Paragraph with leading and trailing whitespace
still the same paragraph.       


"""

        self.assertEqual(
            [
                "# Heading",
                "## Heading 2",
                "Paragraph with leading and trailing whitespace\nstill the same paragraph.",
            ],
            markdown_to_blocks(document),
        )

    def test_block_to_block_type_heading(self):
        header1 = "# Heading1"
        header2 = "## Heading2"
        header3 = "### Heading3"
        header4 = "#### Heading4"
        header5 = "##### Heading5"
        header6 = "###### Heading6"
        not_header = "########### Not a header"

        self.assertEqual(block_type_heading, block_to_block_type(header1))
        self.assertEqual(block_type_heading, block_to_block_type(header2))
        self.assertEqual(block_type_heading, block_to_block_type(header3))
        self.assertEqual(block_type_heading, block_to_block_type(header4))
        self.assertEqual(block_type_heading, block_to_block_type(header5))
        self.assertEqual(block_type_heading, block_to_block_type(header6))

        self.assertEqual(block_type_paragraph, block_to_block_type(not_header))

    def test_block_to_block_type_code(self):
        code_block = "```\nconst greet = 'hello, world';\nconsole.log(greet)\n```"
        self.assertEqual(block_type_code, block_to_block_type(code_block))

    def test_block_to_block_type_quote(self):
        quote = '>"What is a man?"\n>\t\tDracula'
        self.assertEqual(block_type_quote, block_to_block_type(quote))

    def test_block_to_block_type_ordered_list(self):
        ol = "1. First\n2. \nSecond\n3. Last\nItem"
        self.assertEqual(block_type_ordered_list, block_to_block_type(ol))

    def test_block_to_block_type_unordered_list(self):
        ul = "* First\n* \nSecond\n* Last\nItem"
        self.assertEqual(block_type_unordered_list, block_to_block_type(ul))
