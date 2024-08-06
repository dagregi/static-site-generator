import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"',
            node.props_to_html(),
        )

    def test_props_to_html2(self):
        node = HTMLNode(
            "a",
            "boot.dev",
            None,
            {"class": "link link-bold", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="link link-bold" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            None,
            None,
            {"class": "text-block text-center", "id": "main_div"},
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(
            node.props, {"class": "text-block text-center", "id": "main_div"}
        )

    def test_repr(self):
        node = HTMLNode("p", "Paragraph tag")
        self.assertEqual("HTMLNode(p, Paragraph tag, children: None, None)", repr(node))

    def test_leaf_node(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        leaf_node2 = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
        self.assertEqual("<p>This is a paragraph of text.</p>", leaf_node.to_html())
        self.assertEqual('<a href="https://boot.dev">Click me!</a>', leaf_node2.to_html())


if __name__ == "__main__":
    unittest.main()
