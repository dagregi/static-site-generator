import textnode


def main():
    node = textnode.TextNode("Terminus", "italic", "https://terminus.io")
    print(node.__repr__())


main()
