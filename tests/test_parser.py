import unittest

from src.textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_bold,
    text_type_italic,
)
from src.parser import split_nodes_delimiter


class TestNodeDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode(
            "This is text with has **one** and **two** bolded words", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(
            [
                TextNode("This is text with has ", text_type_text),
                TextNode("one", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("two", text_type_bold),
                TextNode(" bolded words", text_type_text),
            ],
            new_nodes,
        )

    def test_multiple_codes(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        node1 = TextNode("Another `inline code`.", text_type_text)
        new_nodes = split_nodes_delimiter([node, node1], "`", text_type_code)
        self.assertEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
                TextNode("Another ", text_type_text),
                TextNode("inline code", text_type_code),
                TextNode(".", text_type_text),
            ],
            new_nodes,
        )

    def test_italic_bold(self):
        node = TextNode("**one bold** and *another italic*", text_type_text)
        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter([node], "**", text_type_bold), "*", text_type_italic
        )
        self.assertEqual(
            [
                TextNode("one bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another italic", text_type_italic),
            ],
            new_nodes,
        )
