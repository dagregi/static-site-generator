import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        self.assertEqual(
            '<a href="https://boot.dev">Click me!</a>', leaf_node2.to_html()
        )

    def test_parent_node(self):
        leaf_node = LeafNode(None, "This is a text.")
        leaf_node2 = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
        parent_node = ParentNode("div", [leaf_node, leaf_node2])
        self.assertEqual(
            '<div>This is a text.<a href="https://boot.dev">Click me!</a></div>',
            parent_node.to_html(),
        )
    def test_parent_node_nesting(self):
        leaf_node = LeafNode("b", "Bold")
        leaf_node2 = LeafNode("i", "Italic")
        leaf_node3 = LeafNode(None, "Look ma no tags!")
        parent_node = ParentNode("p", [leaf_node, leaf_node2])
        parent_node2 = ParentNode("div", [leaf_node3, parent_node])
        self.assertEqual("<div>Look ma no tags!<p><b>Bold</b><i>Italic</i></p></div>", parent_node2.to_html())


if __name__ == "__main__":
    unittest.main()
