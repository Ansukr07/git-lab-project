"""
Duplicate File Finder
=====================

A utility to scan a directory recursively and identify duplicate files
based on their content (MD5 hash), not just filenames.

Features:
- recursive scanning.
- MD5 hashing for content verification.
- Option to delete duplicates (interactive or auto).
- Size filtering (skip small/large files).

Author: Ansu Kumar
Version: 1.0.0
Date: 2025-12-17
"""

import os
import hashlib
import argparse
import logging
import sys
from collections import defaultdict

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("DupFinder")

# Chunk size for reading files to avoid memory issues with large files
CHUNK_SIZE = 8192

def get_file_hash(filepath: str) -> str:
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except OSError as e:
        logger.warning(f"⚠️ Could not read {filepath}: {e}")
        return ""

def find_duplicates(directory: str, min_size: int = 1):
    """
    Scans for duplicates.
    Strategy:
    1. Group files by size (fast).
    2. calculating hash ONLY for files with colliding sizes (slower but accurate).
    """
    directory = os.path.abspath(directory)
    logger.info(f"📂 Scanning: {directory}")

    # Step 1: Group by Size
    size_map = defaultdict(list)
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                size = os.path.getsize(filepath)
                if size >= min_size:
                    size_map[size].append(filepath)
            except OSError:
                continue

    # Step 2: Filter potential duplicates (size > 1 collision)
    potential_duplicates = {size: paths for size, paths in size_map.items() if len(paths) > 1}
    
    if not potential_duplicates:
        logger.info("✅ No duplicates found (based on size).")
        return {}

    logger.info(f"🔎 Found {len(potential_duplicates)} groups of files with same size. Verifying hashes...")

    # Step 3: Verify with Hash
    duplicates = defaultdict(list)
    
    total_potential_groups = len(potential_duplicates)
    processed_groups = 0

    for size, paths in potential_duplicates.items():
        processed_groups += 1
        # Temporary map for this size group: hash -> list of files
        hash_map = defaultdict(list)
        
        for path in paths:
            file_hash = get_file_hash(path)
            if file_hash:
                hash_map[file_hash].append(path)
        
        # Add actual duplicates to result
        for file_hash, file_list in hash_map.items():
            if len(file_list) > 1:
                duplicates[file_hash].extend(file_list)
        
        if processed_groups % 100 == 0:
            print(f"   ...checked {processed_groups}/{total_potential_groups} groups...")

    return duplicates

def main():
    parser = argparse.ArgumentParser(description="Find duplicate files.")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--min-size", type=int, default=1024, help="Minimum file size in bytes (default: 1kb)")
    parser.add_argument("--delete", action="store_true", help="Interactive check to delete duplicates")

    args = parser.parse_args()

    results = find_duplicates(args.directory, args.min_size)

    if not results:
        logger.info("🎉 No duplicates found.")
        sys.exit(0)

    print("\n🚨 DUPLICATES FOUND 🚨")
    print("=" * 40)
    
    count = 0 
    bytes_wasted = 0

    for file_hash, paths in results.items():
        count += 1
        size = os.path.getsize(paths[0])
        wasted = size * (len(paths) - 1)
        bytes_wasted += wasted
        
        print(f"\nGroup {count} [Hash: {file_hash[:8]}...] | Size: {size} bytes | Wasted: {wasted} bytes")
        for i, path in enumerate(paths):
            print(f"  {i+1}: {path}")

        if args.delete:
            keep_idx = input("  👉 Enter number to KEEP (0 to skip, 'all' to keep all): ")
            if keep_idx.isdigit() and 1 <= int(keep_idx) <= len(paths):
                idx = int(keep_idx) - 1
                keep_path = paths[idx]
                print(f"  Keeping: {keep_path}")
                
                for i, path in enumerate(paths):
                    if i != idx:
                        try:
                            os.remove(path)
                            print(f"  🗑️ Deleted: {path}")
                        except OSError as e:
                            print(f"  ❌ Error deleting {path}: {e}")
            else:
                print("  Skipping group.")

    print("=" * 40)
    print(f"Total Groups: {len(results)}")
    print(f"Total Wasted Space: {bytes_wasted / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
