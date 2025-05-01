import os
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline import text_to_textnodes, extract_title
from textnode import TextNode, TextType, text_node_to_html_node
class BlockType(Enum):
    """
    Enum for different block types in a Markdown document.
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    """
    Converts a Markdown document into a list of block strings.

    Args:
        markdown (str): The Markdown document as a string.

    Returns:
        list: A list of block strings.
    """
    blocks = markdown.split("\n\n")
    stripped_blocks = [block.strip() for block in blocks if block.strip()]    

    return stripped_blocks

def block_to_block_type(block):
    """
    Determines the block type of a given block string.

    Args:
        block (str): The block string.

    Returns:
        BlockType: The block type.
    """
    # Split into lines for checks that need to examine each line
    lines = block.split("\n")
    # Check if it starts with 1-6 # followed by a space
    if block.startswith('#'):
    # Count consecutive # characters
        hash_count = 0
        for char in block:
            if char == '#':
                hash_count += 1
            else:
                break
    # Check if 1-6 # followed by a space
        if 1 <= hash_count <= 6 and block[hash_count] == ' ':
            return BlockType.HEADING
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if len(lines) > 0:
        is_ordered_list = True
        for i, line in enumerate(lines, 1):
            expected_prefix = f"{i}. "
            if not line.startswith(expected_prefix):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_types = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # Process each block type individually if needed
        # Example: print or log the block type
        # print(f"Processing block: {block}, Type: {block_type}")
        blocks_types.append(block_type)
    html_nodes = []
    for block, block_type in zip(blocks, blocks_types):

        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(ParentNode(tag="p", children=text_to_children(block)))

        elif block_type == BlockType.HEADING:
            level = block.count("#")
            html_nodes.append(ParentNode(tag=f"h{level}", children=text_to_children(block[level:].strip())))

        elif block_type == BlockType.CODE:
            # Extract the content between the triple backticks
            code_lines = block.split("\n")[1:-1]
    
            # Join with newlines and ensure there's a trailing newline
            code_content = "\n".join(code_lines) + "\n"
    
            # Create a text node for the code content
            text_node = TextNode(code_content, TextType.TEXT)
    
            # Convert to HTML node
            code_node = text_node_to_html_node(text_node)
    
            # Ensure code_node has the right tag
            code_node.tag = "code"
    
            # Create the pre node with the code node as its child
            html_nodes.append(ParentNode(tag="pre", children=[code_node]))

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_content = ""
            for line in lines:
                if line.startswith("> "):
                    quote_content += line[2:] + "\n"
                else:
                    quote_content += line + "\n"
            html_nodes.append(ParentNode(tag="blockquote", children=text_to_children(quote_content.strip())))
        
        elif block_type == BlockType.UNORDERED_LIST:
            li_nodes = []
            items = block.split("\n")
            for item in items:
                if item.startswith("- "):
                    text = item[2:].strip()
                    children = text_to_children(text)
                    li_nodes.append(ParentNode(tag="li", children=children))
            if li_nodes:
                html_nodes.append(ParentNode(tag="ul", children=li_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            ol_nodes = []
            for item in items:
                if item[0].isdigit() and item[1] == ".":
                    text = item[2:].strip()
                    children = text_to_children(text)
                    ol_nodes.append(ParentNode(tag="li", children=children))
            if ol_nodes:
                html_nodes.append(ParentNode(tag="ol", children=ol_nodes))
    html_parent = ParentNode(tag="div", children=html_nodes)

    return html_parent

def text_to_children(text):
    """
    Converts a text string into a list of HTMLNode objects.
    """
    # For paragraphs, replace newlines with spaces
    normalized_text = text.replace("\n", " ")
    # Process the text as a whole
    text_nodes = text_to_textnodes(normalized_text)
    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generates an HTML page from a Markdown file using a template.

    Args:
        from_path (str): The path to the Markdown file.
        template_path (str): The path to the HTML template file.
        dest_path (str): The destination path for the generated HTML file.
    """
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    # Read the Markdown content
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    # Read the template content
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert Markdown to HTML nodes
    html_node = markdown_to_html_node(markdown_content)
    # Convert the HTML nodes to HTML strings
    html_content = html_node.to_html()
    title = extract_title(markdown_content)


    # Replace the placeholder in the template with the generated HTML
    html_content = template_content.replace("{{ Content }}", html_content)
    # Replace the placeholder in the template with the title
    html_content = html_content.replace("{{ Title }}", title)
    # Replace the href="{{ href }}" with the path to the file
    html_content = html_content.replace('href="/', f'href="{basepath}')
    html_content = html_content.replace('src="/', f'src="{basepath}')
    # Write the generated HTML content to the destination file
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(html_content)