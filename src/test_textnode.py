import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

    def test_eq_one(self):
        node = TextNode("this is a text node", TextType.link, "http://8888")
        node2 = TextNode("this is a text node", TextType.link, "http://8888")
        self.assertEqual(node, node2)

    def test_eq_two(self):
        node = TextNode("this is like a text node", TextType.code)
        node2 = TextNode("this is an italicized node", TextType.italic)
        self.assertNotEqual(node, node2)

    def test_eq_three(self):
        node = TextNode("this is a text node", TextType.bold)
        node2 = TextNode("this is a text node with a link", TextType.link, "http://8888")
        self.assertNotEqual(node, node2)


    def test_text_to_leave(self):
        node = TextNode("This is a text node", TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_node_converstion(self):
        node = TextNode("all about text", TextType.bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "all about text")

    def test_node_converstion_two(self):
        node = TextNode("all about text", TextType.italic)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "all about text")

    def test_node_converstion_three(self):
        node = TextNode("all about text", TextType.code)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "all about text")

    def test_node_converstion_four(self):
        node = TextNode("all about text", TextType.link, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "all about text")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_node_converstion_five(self):
        node = TextNode("I'm an image", TextType.image, "source_image")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "source_image", "alt": "I'm an image"})

if __name__ == "__main__":
    unittest.main()
