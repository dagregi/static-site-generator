import unittest

from src.htmlnode import LeafNode, ParentNode
from src.block_parser import (
    block_to_block_type,
    code_to_htmlnode,
    heading_to_htmlnode,
    list_to_htmlnode,
    markdown_to_blocks,
    block_type_heading,
    block_type_paragraph,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_htmlnode,
    paragraph_to_htmlnode,
    quote_to_htmlnode,
)


class TestBlockParser(unittest.TestCase):
    def test_markdown_to_htmlnode(self):
        document = """# Title

This is a paragraph with **bold** and *italic* words.

* First item
* Last item

## Subtitle

```
fn main() {
    let greet = "Hello from Rust!";
    println!("{}", greet);
}
```

## **Bold** Subtitle

1. Build `cargo build`
2. Run `cargo run`

>Never forget the cats.
>![cat](https://randomcats.com)"""
        node = markdown_to_htmlnode(document)
        self.assertEqual("div", node.tag)
        self.assertEqual(
            [
                ParentNode("h1", [LeafNode(None, "Title", None)], None),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is a paragraph with ", None),
                        LeafNode("b", "bold", None),
                        LeafNode(None, " and ", None),
                        LeafNode("i", "italic", None),
                        LeafNode(None, " words.", None),
                    ],
                    None,
                ),
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "First item", None)], None),
                        ParentNode("li", [LeafNode(None, "Last item", None)], None),
                    ],
                    None,
                ),
                ParentNode("h2", [LeafNode(None, "Subtitle", None)], None),
                ParentNode(
                    "pre",
                    [
                        LeafNode(
                            "code",
                            '\nfn main() {\n    let greet = "Hello from Rust!";\n    println!("{}", greet);\n}\n',
                            None,
                        )
                    ],
                    None,
                ),
                ParentNode(
                    "h2",
                    [LeafNode("b", "Bold", None), LeafNode(None, " Subtitle", None)],
                    None,
                ),
                ParentNode(
                    "ol",
                    [
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "Build ", None),
                                LeafNode("code", "cargo build", None),
                            ],
                            None,
                        ),
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "Run ", None),
                                LeafNode("code", "cargo run", None),
                            ],
                            None,
                        ),
                    ],
                    None,
                ),
                ParentNode(
                    "blockquote",
                    [
                        LeafNode(None, "Never forget the cats.\n", None),
                        LeafNode(
                            "img", None, {"src": "https://randomcats.com", "alt": "cat"}
                        ),
                    ],
                    None,
                ),
            ],
            node.children,
        )

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

    def test_heading_to_htmlnode(self):
        header = "#### Custom **heading**"
        node = heading_to_htmlnode(header)
        self.assertEqual("h4", node.tag)
        self.assertEqual(
            [
                LeafNode(None, "Custom ", None),
                LeafNode("b", "heading", None),
            ],
            node.children,
        )

    def test_paragraph_to_htmlnode(self):
        block = "A paragraph with **bold** and *italic* words."
        node = paragraph_to_htmlnode(block)

        self.assertEqual("p", node.tag)
        self.assertEqual(
            [
                LeafNode(None, "A paragraph with ", None),
                LeafNode("b", "bold", None),
                LeafNode(None, " and ", None),
                LeafNode("i", "italic", None),
                LeafNode(None, " words.", None),
            ],
            node.children,
        )

    def test_code_to_htmlnode(self):
        code_block = "```\nconst greet = 'hello, world';\nconsole.log(greet)\n```"
        node = code_to_htmlnode(code_block)

        self.assertEqual("pre", node.tag)
        self.assertEqual(
            [
                LeafNode(
                    "code",
                    "\nconst greet = 'hello, world';\nconsole.log(greet)\n",
                    None,
                ),
            ],
            node.children,
        )

    def test_quote_to_htmlnode(self):
        quote = ">This is a **bold quote**\n>Is this a *italic*?\n>A very famous person"
        node = quote_to_htmlnode(quote)
        self.assertEqual("blockquote", node.tag)
        self.assertEqual(
            [
                LeafNode(None, "This is a ", None),
                LeafNode("b", "bold quote", None),
                LeafNode(None, "\nIs this a ", None),
                LeafNode("i", "italic", None),
                LeafNode(None, "?\nA very famous person", None),
            ],
            node.children,
        )

    def test_ul_to_htmlnode(self):
        ul = "* First **bold**\n* Second *italic*\n* Last `code`"
        node = list_to_htmlnode(ul, "ul")
        self.assertEqual("ul", node.tag)
        self.assertEqual(
            [
                ParentNode(
                    "li",
                    [LeafNode(None, "First ", None), LeafNode("b", "bold", None)],
                    None,
                ),
                ParentNode(
                    "li",
                    [LeafNode(None, "Second ", None), LeafNode("i", "italic", None)],
                    None,
                ),
                ParentNode(
                    "li",
                    [LeafNode(None, "Last ", None), LeafNode("code", "code", None)],
                    None,
                ),
            ],
            node.children,
        )

    def test_ol_to_htmlnode(self):
        ol = "1. First **bold**\n2. Second *italic*\n3. Last `code`"
        node = list_to_htmlnode(ol, "ol")
        self.assertEqual("ol", node.tag)
        self.assertEqual(
            [
                ParentNode(
                    "li",
                    [LeafNode(None, "First ", None), LeafNode("b", "bold", None)],
                    None,
                ),
                ParentNode(
                    "li",
                    [LeafNode(None, "Second ", None), LeafNode("i", "italic", None)],
                    None,
                ),
                ParentNode(
                    "li",
                    [LeafNode(None, "Last ", None), LeafNode("code", "code", None)],
                    None,
                ),
            ],
            node.children,
        )
