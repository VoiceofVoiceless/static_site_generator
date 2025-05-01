import unittest
from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, extract_title

class TestInlineMarkdown(unittest.TestCase):
    
    def test_split_with_code(self):
        # Test code blocks with backticks
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_with_bold(self):
        # Test bold text with double asterisks
        node = TextNode("This is text with a **bold phrase** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold phrase")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        # Test with a single link
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], extract_markdown_links(text))

        text1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text1))

    def test_split_nodes_image(self):
        # Test with a single image
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, {"src": "https://i.imgur.com/zjjcJKZ.png"})

        # Test with multiple images
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/another.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, {"src": "https://i.imgur.com/zjjcJKZ.png"})
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "another image")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].url, {"src": "https://i.imgur.com/another.png"})


    def test_split_nodes_link(self):
        # Test with a single link
        node = TextNode("This is text with a [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, {"href": "https://www.boot.dev"})

        # Test with multiple links
        node = TextNode("This is text with a [link](https://www.boot.dev) and [another link](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, {"href": "https://www.boot.dev"})
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "another link")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].url, {"href": "https://www.google.com"})


    def test_text_to_textnodes(self):
    
        # Test with a mix of formatting
        text = "This is **bold** and _italic_ text with `code`"
        nodes = text_to_textnodes(text)
    
        # Check that we got the expected number of nodes
        self.assertEqual(len(nodes), 6)

        # Check each node's properties
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
    
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
    
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)

        self.assertEqual(nodes[4].text, " text with ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)

        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
       
    def test_extract_title(self):
    # Test with a valid markdown
        assert extract_title("# Hello World") == "Hello World"
    
    # Test with leading/trailing spaces
        assert extract_title("# Hello World  ") == "Hello World"
    
    # Test with no title
        try:
            extract_title("Hello World")
            assert False, "Should have raised an exception"
        except ValueError:
            pass
    
    # Test with invalid markdown
        try:
            extract_title("## Hello World")
            assert False, "Should have raised an exception"
        except ValueError:
            pass
    # Test with empty string
        try:
            extract_title("")
            assert False, "Should have raised an exception"
        except ValueError:
            pass
    # Test with only spaces
        try:
            extract_title("   ")
            assert False, "Should have raised an exception"
        except ValueError:
            pass
    # Test with no leading hash
        try:
            extract_title("Hello World")
            assert False, "Should have raised an exception"
        except ValueError:
            pass
    # Test with multiple hashes
        try:
            extract_title("### Hello World")
            assert False, "Should have raised an exception"
        except ValueError:
            pass
    # Test with special characters
        assert extract_title("# Hello @World!") == "Hello @World!"
    # Test with unicode characters
        assert extract_title("# Hello 世界") == "Hello 世界"
    # Test with emojis
        assert extract_title("# Hello 🌍") == "Hello 🌍"
        


if __name__ == "__main__":
    unittest.main()
# This code is a test suite for the inline.py module, which contains functions to process and extract information from markdown text.
# The test suite uses the unittest framework to define a series of tests that check the functionality of the functions in the inline.py module.
# The tests cover splitting text nodes based on delimiters (like backticks for code, double asterisks for bold, etc.), extracting markdown images and links, and ensuring that the output is as expected.
# The test suite also includes tests for the TextNode class, which represents a node of text with a specific type (like text, bold, italic, etc.) and properties (like href for links).
# The tests check for equality and conversion of TextNode objects to HTML nodes.
# The test suite is designed to ensure that the functions in the inline.py module work correctly and produce the expected output for various input cases.