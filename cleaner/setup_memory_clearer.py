# setup_memory_clearer.py
import os
import sys
import shutil
from pathlib import Path

def create_folder_structure():
    """Create the folder structure for Memory Clearer"""
    
    # Create main "clear" folder
    clear_folder = Path("clear")
    clear_folder.mkdir(exist_ok=True)
    
    # Create subfolders
    folders = [
        "backups",
        "logs",
        "cache",
        "temp_cleanup",
        "config"
    ]
    
    for folder in folders:
        (clear_folder / folder).mkdir(exist_ok=True)
    
    # Create README file
    readme_path = clear_folder / "README.txt"
    with open(readme_path, 'w') as f:
        f.write("""Memory Clearer Tool
=====================

This tool helps manage system memory and prevent crashes.

Folders:
- backups/: Store backup files
- logs/: Activity logs
- cache/: Temporary cache files
- temp_cleanup/: Temporary cleanup files
- config/: Configuration files

How to use:
1. Run memory_clearer.py to start the GUI
2. Click "Clean Memory Now" for quick cleanup
3. Use "Deep Clean" for thorough cleanup
4. Enable monitoring for automatic alerts

System Requirements:
- Windows/Linux/Mac
- Python 3.6+
- psutil library

Created for memory management and system stability.
""")
    
    # Create a batch file for Windows
    if sys.platform == 'win32':
        batch_path = clear_folder / "run_memory_clearer.bat"
        with open(batch_path, 'w') as f:
            f.write("""@echo off
echo Starting Memory Clearer Tool...
python memory_clearer.py
pause
""")
    
    # Create a shell script for Linux/Mac
    else:
        shell_path = clear_folder / "run_memory_clearer.sh"
        with open(shell_path, 'w') as f:
            f.write("""#!/bin/bash
echo "Starting Memory Clearer Tool..."
python3 memory_clearer.py
read -p "Press any key to exit..."
""")
        os.chmod(shell_path, 0o755)
    
    print("✅ Folder structure created successfully!")
    print(f"📁 Main folder: {clear_folder.absolute()}")
    print("\nContents:")
    for item in clear_folder.iterdir():
        if item.is_dir():
            print(f"  📁 {item.name}/")
        else:
            print(f"  📄 {item.name}")

def create_requirements_file():
    """Create requirements.txt"""
    with open("requirements.txt", 'w') as f:
        f.write("""psutil>=5.8.0
tkinter  # built-in
""")
    
    print("✅ Created requirements.txt")

def install_requirements():
    """Install required packages"""
    try:
        import psutil
        print("✅ psutil already installed")
    except ImportError:
        print("📦 Installing psutil...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        print("✅ psutil installed successfully")

def main():
    print("Memory Clearer - Setup Tool")
    print("=" * 50)
    
    # Create folder structure
    create_folder_structure()
    
    # Create requirements file
    create_requirements_file()
    
    # Install requirements
    install_requirements()
    
    print("\n" + "=" * 50)
    print("Setup complete! 🎉")
    print("To use the tool:")
    print("  1. Navigate to the 'clear' folder")
    print("  2. Run: python memory_clearer.py")
    print("  3. Or run the batch/shell script")
    
if __name__ == "__main__":
    main()