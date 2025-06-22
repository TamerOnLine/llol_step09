import os
import re

README_PATH = "README.md"
OUTPUT_PATH = "docs/index.md"
LICENSE_LINK = "https://github.com/PostgresCraft/encryption_service/blob/main/LICENSE"

def read_readme(path=README_PATH):
    """
    Read the content of the README file.

    Args:
        path (str): Path to the README file.

    Returns:
        str: Content of the README file.
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def clean_content(content: str) -> str:
    """
    Clean unwanted sections from README content.

    This removes direct display links, 'Back to Top' links, and
    the table of contents section.

    Args:
        content (str): Raw README content.

    Returns:
        str: Cleaned README content.
    """
    content = re.sub(r".*?\[Live Documentation\]\([^)]+\)\s*\n?", "", content)
    content = re.sub(r"\[.*?Back to Top.*?\]\([^)]+\)\s*\n?", "", content, flags=re.IGNORECASE)
    content = re.sub(r"## Table of Contents[\s\S]+?(?=\n## )", "", content)
    return content

def fix_links(content: str) -> str:
    """
    Fix or update internal and external links in the content.

    Args:
        content (str): Cleaned README content.

    Returns:
        str: Content with updated links.
    """
    content = content.replace("screenshots/", "screenshots/")
    content = content.replace("(../LICENSE)", f"({LICENSE_LINK})")
    content = content.replace("(LICENSE)", f"({LICENSE_LINK})")
    return content

def write_to_docs(content: str, output_path=OUTPUT_PATH):
    """
    Write processed content to the documentation output file.

    Args:
        content (str): Final markdown content to write.
        output_path (str): Destination path for the output file.
    """
    # Remove excess whitespace from top and bottom
    lines = content.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    content = '\n'.join(lines)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

def main():
    """
    Main function to process README and write cleaned content to documentation.
    """
    print("Reading README.md...")
    content = read_readme()

    print("Cleaning content...")
    content = clean_content(content)

    print("Fixing links...")
    content = fix_links(content)

    print(f"Saving to {OUTPUT_PATH}...")
    write_to_docs(content)

    print("README.md has been successfully converted to docs/index.md.")

if __name__ == "__main__":
    main()
