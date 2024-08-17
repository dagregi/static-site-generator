import os
import shutil

from block_parser import (
    block_to_block_type,
    markdown_to_blocks,
    block_type_heading,
    markdown_to_htmlnode,
)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r").read()
    template = open(template_path, "r").read()
    dest = open(f"{dest_path}", "w")

    full_html = template.replace("{{ Title }}", extract_title(markdown)).replace(
        "{{ Content }}", markdown_to_htmlnode(markdown).to_html()
    )

    dest.write(full_html)
    dest.close()


def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if (
            block_to_block_type(block) == block_type_heading
            and len(block.split(" ", 1)[0]) == 1
        ):
            return block.split(" ", 1)[1]
    raise Exception("Title not found")


def copy_contents(from_dir, to_dir):
    def copy(fro, to):
        for item in os.listdir(fro):
            print(f"Copying: {fro}/{item} to {to_dir}/{item}")
            if os.path.isfile(f"{fro}/{item}"):
                shutil.copy(f"{fro}/{item}", to)
            else:
                os.mkdir(f"{to}/{item}")
                copy(f"{fro}/{item}", f"{to}/{item}")

    if not os.path.exists(to_dir):
        print(f"Creating {to_dir} directory")
        os.mkdir(to_dir)
    if os.path.getsize(to_dir) != 0:
        for item in os.listdir(to_dir):
            print(f"Removing: {to_dir}/{item}")
            if os.path.isfile(f"{to_dir}/{item}"):
                os.remove(f"{to_dir}/{item}")
            else:
                shutil.rmtree(f"{to_dir}/{item}")
    copy(from_dir, to_dir)
