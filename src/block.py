from enum import Enum


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