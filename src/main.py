from textnode import TextNode, TextType
import os
import shutil

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

    

def main():
    copy_from_source_to_destination("static", "public")

if __name__ == "__main__":
    main()

