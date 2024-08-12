import unittest

from src.textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_bold,
    text_type_italic,
    text_type_image,
    text_type_link,
)
from src.inline_parser import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnode,
)


class TestInlineParser(unittest.TestCase):
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

    def test_image_extractor(self):
        line = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(line),
        )

    def test_link_extractor(self):
        line = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_links(line),
        )

    def test_node_links(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_node_images(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnode(text)
        self.assertEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode(
                    "obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )
