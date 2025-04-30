import unittest
from block import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline import text_to_textnodes

class TestHTMLNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is a **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
        [
            "This is a **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

    def test_markdown_to_blocks_2(self):
        md = """
This is a **bolded** paragraph that I edited to contain more text!!

This is another paragraph with _italic_ text and `code` here, plus some more **text** maybe?
This is the same paragraph on a new line
and a new line

and a new paragraph with a new ling
new lien

- This is a list
- with **items**
- and some `code` here
- and some more text
- and some more text
- and some more text

- and some more text in a new list?
- and some more text in a new list?
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
        [
            "This is a **bolded** paragraph that I edited to contain more text!!",
            "This is another paragraph with _italic_ text and `code` here, plus some more **text** maybe?\nThis is the same paragraph on a new line\nand a new line",
            "and a new paragraph with a new ling\nnew lien",
            "- This is a list\n- with **items**\n- and some `code` here\n- and some more text\n- and some more text\n- and some more text",
            "- and some more text in a new list?\n- and some more text in a new list?",
        ],
    )
        
    def test_markdown_to_blocks_3(self):
        md = """
This is a **bolded** paragraph that I edited to contain more text!!

This is another paragraph with _italic_ text and `code` here, plus some more **text** maybe?
This is the same paragraph on a new line
and a new line

and a new paragraph with a new ling
new lien

- This is a list
- with **items**
- and some `code` here
- and some more text
- and some more text
- and some more text

- and some more text in a new list?
- and some more text in a new list?


This paragraph is not part of the list but does have a double new line between it and the list.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
        [
            "This is a **bolded** paragraph that I edited to contain more text!!",
            "This is another paragraph with _italic_ text and `code` here, plus some more **text** maybe?\nThis is the same paragraph on a new line\nand a new line",
            "and a new paragraph with a new ling\nnew lien",
            "- This is a list\n- with **items**\n- and some `code` here\n- and some more text\n- and some more text\n- and some more text",
            "- and some more text in a new list?\n- and some more text in a new list?",
            "This paragraph is not part of the list but does have a double new line between it and the list.",
        ],
    )
        
    def test_block_to_block_type(self):
        blocks =["# This is a **bolded** paragraph that I edited to contain more text!!",
            "```This is another paragraph with _italic_ text and `code` here, plus some more **text** maybe?\nThis is the same paragraph on a new line\nand a new line```",
            ">and a new paragraph with a new ling\n>new lien",
            "- This is a list\n- with **items**\n- and some `code` here\n- and some more text\n- and some more text\n- and some more text",
            "-and some more text in a new list?\n- and some more text in a new list?",
            "1. This paragraph is not part of the list but does have a double new line between it and the list.\n2. Now it is an ordered list.",]
        type_of_blocks = []
        for block in blocks:
            type_of_blocks.append(block_to_block_type(block))
        self.assertEqual(
    type_of_blocks,
    [
        BlockType.HEADING,
        BlockType.CODE,
        BlockType.QUOTE,
        BlockType.UNORDERED_LIST,
        BlockType.PARAGRAPH,
        BlockType.ORDERED_LIST,
    ],
)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )