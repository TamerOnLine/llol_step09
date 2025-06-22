import subprocess
import sys
import os

def ensure_virtualenv():
    if sys.prefix == sys.base_prefix:
        print("❌ You are not inside a virtual environment (venv).")
        print("👉 Please activate it first using:")
        if os.name == "nt":
            print("   .\\venv\\Scripts\\Activate")
        else:
            print("   source venv/bin/activate")
        sys.exit(1)

def run_command(description, command, shell=False):
    print(f"\n🔧 {description}...\n")
    try:
        subprocess.run(command, check=True, shell=shell)
        print(f"✅ Done: {description}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description}\n{e}")
        sys.exit(1)

def show_menu():
    print("\n🔐 indexMD Control Panel")
    print("==========================")
    print("1. 📦 Build documentation")
    print("2. 🧽 Prepare docs only")
    print("3. 🌐 Serve locally")
    print("4. 🚀 Deploy to GitHub Pages")
    print("5. 🔍 Show version")
    print("0. ❌ Exit")
    print("==========================")

def main():
    ensure_virtualenv()

    while True:
        show_menu()
        choice = input("Enter your choice (0-5): ").strip()

        if choice == "1":
            run_command("Building full documentation", [sys.executable, "build_all.py"])
        elif choice == "2":
            run_command("Preparing docs from README", [sys.executable, "prepare_docs.py"])
        elif choice == "3":
            run_command("Launching local MkDocs server", ["mkdocs", "serve"])
        elif choice == "4":
            run_command("Deploying to GitHub Pages", ["mkdocs", "gh-deploy"])
        elif choice == "5":
            print("📦 indexMD CLI v1.0.0")
        elif choice == "0":
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please enter a number from 0 to 5.")

if __name__ == "__main__":
    main()
