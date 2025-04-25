print("hello world")
from textnode import TextNode, TextType

def main():
    dummy_node = TextNode("This is some anchor text", TextType.link, "https://www.boot.dev")
    print (dummy_node)

if __name__ == "__main__":
    main()

