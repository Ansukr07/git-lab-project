"""
Intelligent File Organizer
==========================

A sophisticated script to reorganize filesystem clutter by sorting files into
categorized directories based on their extensions. It supports exclusion lists,
dry runs, and comprehensive reporting.

Author: Ansu Kumar
Version: 3.0.0
__version_info__ = (3, 0, 0)
Date: 2025-12-17
"""

import os
import shutil
import argparse
import logging
import sys
import time
from typing import List, Dict, Set
from datetime import datetime

# --- CONFIGURATION MAP ---
# Defines the mapping between file types and their extensions.
EXTENSION_MAP: Dict[str, List[str]] = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff", ".webp",
        ".ico", ".heic", ".raw"
    ],
    "Documents": [
        ".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".xlsx", ".xls",
        ".pptx", ".ppt", ".csv", ".md", ".json", ".xml", ".epub", ".log"
    ],
    "Videos": [
        ".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v",
        ".3gp", ".mpeg", ".mpg"
    ],
    "Music": [
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff"
    ],
    "Archives": [
        ".zip", ".rar", ".tar", ".gz", ".7z", ".bz2", ".xz", ".iso", ".tgz"
    ],
    "Scripts": [
        ".py", ".js", ".sh", ".bat", ".ps1", ".cpp", ".java", ".c", ".h",
        ".html", ".css", ".php", ".rb", ".go", ".ts", ".pl"
    ],
    "Executables": [
        ".exe", ".msi", ".apk", ".app", ".bin", ".jar", ".deb", ".rpm"
    ],
    "Datasets": [
        ".sql", ".db", ".sqlite", ".db3", ".parquet", ".hdf5"
    ]
}

# Files that should never be moved
IGNORED_FILES: Set[str] = {
    "organize_files.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
    ".git",
    "LICENSE",
    "organization_report.txt"
}

# --- LOGGER CONFIG ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("FileOrganizer")

class OrganizationReport:
    """
    Handles generation of the post-cleanup report.
    """
    def __init__(self):
        self.moves: List[str] = []
        self.errors: List[str] = []
        self.start_time = datetime.now()

    def record_move(self, filename: str, category: str):
        self.moves.append(f"MOVED: {filename} -> {category}/")

    def record_error(self, filename: str, error: str):
        self.errors.append(f"ERROR: {filename} - {error}")

    def save_to_file(self, directory: str):
        path = os.path.join(directory, "organization_report.txt")
        duration = datetime.now() - self.start_time
        
        with open(path, "w", encoding='utf-8') as f:
            f.write("FILE ORGANIZATION REPORT\n")
            f.write("========================\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Duration: {duration}\n")
            f.write(f"Total Moves: {len(self.moves)}\n")
            f.write(f"Total Errors: {len(self.errors)}\n\n")
            
            f.write("DETAILS:\n")
            f.write("-" * 20 + "\n")
            for move in self.moves:
                f.write(move + "\n")
            
            if self.errors:
                f.write("\nERRORS:\n")
                f.write("-" * 20 + "\n")
                for err in self.errors:
                    f.write(err + "\n")
        
        logger.info(f"📄 Report saved to: {path}")

def get_category_for_file(filename: str) -> str:
    """
    Determines the category based on extension.
    """
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    
    return "Others"

def organize_directory(directory: str, dry_run: bool = False):
    """
    Main logic to organize the directory.
    """
    directory = os.path.abspath(directory)
    
    if not os.path.exists(directory):
        logger.error(f"❌ Directory not found: {directory}")
        return

    logger.info(f"🚀 Starting organization in: {directory}")
    if dry_run:
        logger.warning("🚧 DRY RUN ENABLED - No changes will be applied.")

    report = OrganizationReport()
    
    # Pre-calculate files to avoid modification during iteration issues
    files_to_process = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    for filename in files_to_process:
        if filename in IGNORED_FILES or filename.startswith("."):
            logger.debug(f"Skipping ignored file: {filename}")
            continue

        category = get_category_for_file(filename)
        source_path = os.path.join(directory, filename)
        category_dir = os.path.join(directory, category)
        dest_path = os.path.join(category_dir, filename)

        if dry_run:
            logger.info(f"🔎 [Dry Run] Would move: {filename} -> {category}/")
            continue

        try:
            # Create Category Directory
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
                logger.debug(f"Created directory: {category_dir}")

            # Handle Name Collision
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                timestamp = int(time.time())
                new_filename = f"{base}_{timestamp}{ext}"
                dest_path = os.path.join(category_dir, new_filename)
                logger.warning(f"⚠️ Collision detected. Renaming to: {new_filename}")

            shutil.move(source_path, dest_path)
            report.record_move(filename, category)
            logger.info(f"✅ Moved: {filename} -> {category}/")

        except Exception as e:
            error_msg = str(e)
            report.record_error(filename, error_msg)
            logger.error(f"❌ Failed to move {filename}: {error_msg}")

    # Finalize
    if not dry_run:
        report.save_to_file(directory)
        logger.info("🎉 Organization complete! Check report for details.")
    else:
        logger.info("🚧 Dry run finished.")

def main():
    """
    CLI Entry Point.
    """
    parser = argparse.ArgumentParser(
        description="Organize your files into neat categories.",
        epilog="Use with caution in system directories."
    )
    
    parser.add_argument("directory", nargs="?", default=".", help="Target directory (default: current)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without moving files")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation prompt")
    
    args = parser.parse_args()

    # Safety Prompt
    if not args.dry_run and not args.confirm:
        print(f"⚠️  WARNING: You are about to reorganize: {os.path.abspath(args.directory)}")
        print("   This will move files into subfolders.")
        response = input("   Are you sure? (type 'yes' to proceed): ")
        if response.lower() != 'yes':
            print("❌ Operation cancelled by user.")
            sys.exit(0)

    organize_directory(args.directory, args.dry_run)

if __name__ == "__main__":
    main()
