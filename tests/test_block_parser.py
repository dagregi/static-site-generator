import unittest

from src.block_parser import markdown_to_blocks


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
