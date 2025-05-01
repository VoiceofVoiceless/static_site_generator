from textnode import TextType, TextNode
from htmlnode import LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        # If the node is not a text node, keep it as is
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        # Split the text by delimiter
        parts = old_node.text.split(delimiter)
        
        # If there's only one part, no delimiter was found
        if len(parts) == 1:
            result.append(old_node)
            continue

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: unmatched {delimiter}")
            
        # Now we need to create nodes with alternating types
        # How would you do this?
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    result.append(TextNode(part, TextType.TEXT))

            else:
                if part:
                    result.append(TextNode(part, text_type))

    return result

def extract_markdown_images(text):
    #return a list of tuples containing the alt text and URL of the related images extracted
    list_of_tuples = []
    list_of_tuples = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return list_of_tuples

def extract_markdown_links(text):
    #extract markdown links and return tuples of anchor text and urls
    list_of_tuples = []
    list_of_tuples = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return list_of_tuples

def extract_title(markdown):
    #extract the title from the markdown text
    title = ""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            # Remove the leading "# " or "<h1>" and trailing "#"
            title = line[2:].strip()
            break
    if not title:
        raise ValueError("Invalid markdown syntax: title not found")

    return title

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if not extract_markdown_images(node.text):
            result.append(node)
        else:
            current_text = node.text
            sections = []
            while extract_markdown_images(current_text):
                list_of_anchor_text_and_images = extract_markdown_images(current_text)
                current_text = current_text.split(f"![{list_of_anchor_text_and_images[0][0]}]({list_of_anchor_text_and_images[0][1]})", 1)
                before_text, after_text = current_text
                current_text = after_text
                if before_text:
                    sections.append(TextNode(before_text, TextType.TEXT))
                sections.append(TextNode(list_of_anchor_text_and_images[0][0], TextType.IMAGE, list_of_anchor_text_and_images[0][1]))
            if current_text:
                    sections.append(TextNode(current_text, TextType.TEXT))
            result += sections    

    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if not extract_markdown_links(node.text):
            result.append(node)
        else:
            current_text = node.text
            sections = []
            while extract_markdown_links(current_text):
                list_of_anchor_text_and_links = extract_markdown_links(current_text)
                current_text = current_text.split(f"[{list_of_anchor_text_and_links[0][0]}]({list_of_anchor_text_and_links[0][1]})", 1)
                before_text, after_text = current_text
                current_text = after_text
                if before_text:
                    sections.append(TextNode(before_text, TextType.TEXT))
                sections.append(TextNode(list_of_anchor_text_and_links[0][0], TextType.LINK, list_of_anchor_text_and_links[0][1]))
            if current_text:
                    sections.append(TextNode(current_text, TextType.TEXT))
            result += sections    

    return result

def text_to_textnodes(text):
    #initialize the text nodes
    nodes = [TextNode(text, TextType.TEXT)]
    # Split nodes by delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # Split the nodes into text and image nodes
    nodes = split_nodes_image(nodes)
    # Split the nodes into text and link nodes
    nodes = split_nodes_link(nodes)
    
        
    return nodes

