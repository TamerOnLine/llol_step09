import os

def create_structure():
    """
    Creates a documentation folder structure with default markdown, CSS, and HTML files.

    Folders Created:
        - docs
        - docs/sections
        - docs/screenshots
        - docs/stylesheets
        - docs/overrides
        - docs/overrides/partials

    Files Created:
        - Markdown documentation files in docs/sections
        - A custom stylesheet in docs/stylesheets
        - A footer partial HTML file in docs/overrides/partials

    Prompts the user before overwriting existing files unless none exist.
    """
    folders = [
        "docs",
        "docs/sections",
        "docs/screenshots",
        "docs/stylesheets",
        "docs/overrides",
        "docs/overrides/partials"
    ]

    files = {
        "docs/index.md": "# Welcome to indexMD Documentation\n",
        "docs/sections/about.md": "## About\nThis section describes the project.",
        "docs/sections/contact.md": "## Contact\nYour contact details here.",
        "docs/sections/important-links.md": "## Important Links\nUseful resources go here.",
        "docs/sections/privacy.md": "## Privacy Policy\nYour privacy matters.",
        "docs/sections/terms.md": "## Terms and Conditions\nUsage terms go here.",
        "docs/stylesheets/extra.css": "/* Custom styles go here */",
        "docs/overrides/partials/footer.html": (
            "<footer>\n  <p>\u00a9 2025 Tamer Online</p>\n</footer>\n"
        )
    }

    # Create directories
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    # Check for existing files
    existing_files = [path for path in files if os.path.exists(path)]
    overwrite_all = True

    if existing_files:
        choice = input(
            f"{len(existing_files)} file(s) already exist. Overwrite all? (y/N): "
        ).strip().lower()
        overwrite_all = (choice == 'y')

    # Create or skip files based on user input
    for path, content in files.items():
        if os.path.exists(path) and not overwrite_all:
            print(f"Skipped existing file: {path}")
            continue

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {path}")


if __name__ == "__main__":
    create_structure()
