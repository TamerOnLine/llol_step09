import os
import re
import subprocess
import sys

README_PATH = "README.md"
OUTPUT_PATH = "docs/index.md"
LICENSE_LINK = "https://github.com/PostgresCraft/encryption_service/blob/main/LICENSE"

def read_readme(path=README_PATH):
    """
    Read the content of the README file.

    Args:
        path (str): Path to the README file.

    Returns:
        str: The content of the README file.
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def clean_content(content: str) -> str:
    """
    Clean the README content by removing live documentation and back-to-top links.

    Args:
        content (str): Raw content from the README file.

    Returns:
        str: Cleaned content.
    """
    content = re.sub(r".*?\[Live Documentation\]\([^)]+\)\s*\n?", "", content)
    content = re.sub(r"\[.*?Back to Top.*?\]\([^)]+\)\s*\n?", "", content, flags=re.IGNORECASE)
    content = re.sub(r"## Table of Contents[\s\S]+?(?=\n## )", "", content)
    return content

def fix_links(content: str) -> str:
    """
    Replace local LICENSE links with full GitHub link and fix image paths.

    Args:
        content (str): Cleaned README content.

    Returns:
        str: Content with fixed links.
    """
    content = content.replace("screenshots/", "screenshots/")
    content = content.replace("(../LICENSE)", f"({LICENSE_LINK})")
    content = content.replace("(LICENSE)", f"({LICENSE_LINK})")
    return content

def write_to_docs(content: str, output_path=OUTPUT_PATH):
    """
    Write the processed content to the documentation path.

    Args:
        content (str): Final processed content.
        output_path (str): Path to write the documentation.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

def run_script(description: str, command: list) -> bool:
    """
    Execute a shell command with logging.

    Args:
        description (str): Description of the command being run.
        command (list): Command to execute.

    Returns:
        bool: True if the command was successful, False otherwise.
    """
    print(f"\n[INFO] {description}...\n")
    try:
        subprocess.run(command, check=True)
        print(f"[SUCCESS] {description} completed.\n")
        return True
    except subprocess.CalledProcessError as error:
        print(f"[ERROR] Failed during {description}: {error}\n")
        return False

def check_virtual_environment():
    """
    Ensure the script is run inside a virtual environment.
    """
    if sys.prefix == sys.base_prefix:
        import platform
        activate_cmd = ".\\venv\\Scripts\\Activate" if platform.system() == "Windows" else "source venv/bin/activate"

        print("[ERROR] Not inside a virtual environment (venv).")
        print(f"[ACTION] Please activate it using:\n  {activate_cmd}\n")
        sys.exit(1)

def main():
    """
    Main function to process README and build documentation.
    """
    check_virtual_environment()

    print("Starting documentation build process...\n")

    run_script("Setting up documentation structure", [sys.executable, "setup_docs_structure.py"])

    if not run_script("Preparing documentation", [sys.executable, "prepare_docs.py"]):
        return

    if not run_script("Building site using MkDocs", ["mkdocs", "build"]):
        return

    print("\nAll steps completed successfully.")

if __name__ == "__main__":
    main()