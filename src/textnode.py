from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.code:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.image:
        return LeafNode("img", None, {"src":text_node.url , "alt":text_node.text})
    else:
        raise Exception("Text node is not a text")
