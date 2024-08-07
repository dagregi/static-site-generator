from src.textnode import TextNode, text_type_text


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        new_nodes.extend(
            (
                TextNode(part, text_type_text)
                if i % 2 == 0
                else TextNode(parts[i], text_type)
            )
            for i, part in enumerate(parts)
            if parts[i] != ""
        )

    return new_nodes
