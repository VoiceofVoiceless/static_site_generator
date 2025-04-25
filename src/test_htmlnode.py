import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_one(self):
        test_dict = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode ("a", "Click me", [], test_dict)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_two(self):
        test_dict_one = {"href": "https://www.google.com",}
        node = HTMLNode ("p", "this is a paragraph", [], test_dict_one)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_three(self):
        test_dict = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode ("h1", "this is a header", [], test_dict)
        self.assertNotEqual(node.props_to_html(), "")

    def test_four(self):
        node = LeafNode ("h1", "this is a header?")
        self.assertEqual(node.to_html(), "<h1>this is a header?</h1>")

    def test_five(self):
        node = LeafNode ("p", "ell, ma!")
        self.assertNotEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_six(self):
        test_dict= {"href": "https://www.google.com", "target": "_blank",}
        node = LeafNode ("a", "Anchor test!", test_dict)
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Anchor test!</a>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)
