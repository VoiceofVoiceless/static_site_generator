from textnode import TextNode, TextType
import os
import shutil
import sys
from block import generate_page
from pathlib import Path


    #recursive function to copy the contents of the source directory to the destination directory
def copy_source(source, destination):
    """Recursively copy files from source to destination."""
    if os.path.isdir(source):
        # Source is a directory, create destination directory if needed
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)
            print(f"Directory created: {destination}")
            
        # Copy each item from source to destination
        for item in os.listdir(source):
            src_path = os.path.join(source, item)
            dst_path = os.path.join(destination, item)
            copy_source(src_path, dst_path)
    else:
        # Source is a file, ensure destination parent directory exists
        dst_dir = os.path.dirname(destination)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
            print(f"Directory created: {dst_dir}")
            
        # Copy the file
        shutil.copy(source, destination)
        print(f"Copied file: {source} copied to {destination}")


def copy_from_source_to_destination(source, destination):
    """
    First deletes all the contents at destination then copies the contents of a source directory to the destination directory.
    
    Args:
        source (str): The path to the source directory.
        destination (str): The path to the destination directory.
    """
    # Check if the source exists
    if not os.path.exists(source):

        raise FileNotFoundError(f"Source directory {source} does not exist.")
    
    if os.path.isfile(source):

        raise IsADirectoryError(f"Source {source} is a file, not a directory.")
    
    if os.path.isfile(destination):
        os.remove(destination)
        print(f"File deleted: {destination}")

    if os.path.isdir(destination):
        shutil.rmtree(destination)
        print(f"Directory deleted: {destination}")

    if not os.path.exists(destination):
        os.makedirs(destination)
        print(f"Directory created: {destination}")

    copy_source(source, destination)

def generate_pages_recursive(content_path, template_path, content_root, destination_root, basepath="/"):
    content_root = Path(content_root).resolve()
    destination_root = Path(destination_root).resolve()
    content_path = Path(content_path).resolve()
    
    for item in content_path.iterdir():
        rel_path = item.relative_to(content_root)
        out_path = destination_root / rel_path
        
        if item.is_dir():
            generate_pages_recursive(item, template_path, content_root, destination_root, basepath)
        elif item.suffix == ".md":
            # For index.md files, place them directly in their parent directory
            if item.stem == "index":
                html_file_path = destination_root / rel_path.parent / "index.html"
            else:
                # For non-index.md files, create a directory with their name
                dir_name = out_path.with_suffix("")
                dir_name.mkdir(parents=True, exist_ok=True)
                html_file_path = dir_name / "index.html"
            
            # Make sure parent directory exists
            html_file_path.parent.mkdir(parents=True, exist_ok=True)
            generate_page(item, template_path, html_file_path, basepath)



def main():
    # Something like this would be better
    basepath = "/" # default value
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_from_source_to_destination("static", "docs")
    generate_pages_recursive("content", "template.html", "content", "docs", basepath)
    print("All files copied and HTML pages generated successfully.")

if __name__ == "__main__":
    main()

