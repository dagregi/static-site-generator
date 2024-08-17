from page_generator import copy_contents, generate_page


def main():
    copy_contents("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")


main()
