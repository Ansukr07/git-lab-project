"""
PDF Merger Utility
==================

This script provides a streamlined interface for merging multiple PDF documents
into a single cohesive file. It supports directory scanning, explicit file lists,
and sorting options to ensure the final document is arranged correctly.

It utilizes the `pypdf` library for reliable PDF manipulation.

Features:
- Merge all PDFs in a directory.
- Merge specific list of files.
- Verbose logging and error handling.
- Encryption awareness (skips or warns on encrypted files).

Author: Ansu Kumar
Version: 1.0.0
Date: 2025-12-17
"""

import os
import argparse
import logging
import sys
from typing import List, Optional
try:
    from pypdf import PdfWriter, PdfReader
    from pypdf.errors import PdfReadError
except ImportError:
    print("❌ Error: 'pypdf' library is missing. Install it via: pip install pypdf")
    sys.exit(1)

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("PDFMerger")

def get_pdf_files(directory: str) -> List[str]:
    """Scans a directory for .pdf files and returns sorted paths."""
    if not os.path.exists(directory):
        logger.error(f"Directory not found: {directory}")
        return []
        
    files = [
        os.path.join(directory, f) 
        for f in os.listdir(directory) 
        if f.lower().endswith(".pdf")
    ]
    files.sort()  # Alphabetical sort by default
    return files

def merge_pdfs(file_list: List[str], output_path: str):
    """
    Merges a list of PDF file paths into a single output file.
    """
    if not file_list:
        logger.warning("No PDF files provided to merge.")
        return

    merger = PdfWriter()
    count = 0
    
    logger.info(f"🚀 Starting merge of {len(file_list)} files...")

    for pdf_path in file_list:
        try:
            # We use PdfReader to append pages
            # In pypdf >= 3.0, PdfWriter has append methods but reading first is safer for validation
            reader = PdfReader(pdf_path)
            
            if reader.is_encrypted:
                logger.warning(f"⚠️ Skipping encrypted file: {pdf_path}")
                continue

            merger.append(reader)
            logger.info(f"  [+] Added: {os.path.basename(pdf_path)} ({len(reader.pages)} pages)")
            count += 1
            
        except PdfReadError:
            logger.error(f"  [-] Corrupt or invalid PDF: {pdf_path}")
        except Exception as e:
            logger.error(f"  [-] Unexpected error processing {pdf_path}: {e}")

    if count == 0:
        logger.error("❌ No files were successfully merged. Aborting write.")
        return

    try:
        with open(output_path, "wb") as f:
            merger.write(f)
        logger.info(f"🎉 Successfully merged {count} files into: {output_path}")
    except IOError as e:
        logger.critical(f"❌ Failed to write output file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Merge multiple PDF files into one.")
    
    parser.add_argument("--dir", help="Directory containing PDFs to merge")
    parser.add_argument("--files", nargs="+", help="Specific list of PDF files to merge")
    parser.add_argument("--output", default="merged_output.pdf", help="Output filename (default: merged_output.pdf)")

    args = parser.parse_args()

    # Determine source
    pdf_files = []
    if args.files:
        pdf_files = args.files
        # Validate existence
        pdf_files = [f for f in pdf_files if os.path.exists(f)]
    elif args.dir:
        pdf_files = get_pdf_files(args.dir)
    else:
        # Default to current directory
        logger.info("No input specified, scanning current directory...")
        pdf_files = get_pdf_files(".")

    if not pdf_files:
        logger.error("No PDF files found to process.")
        sys.exit(1)

    merge_pdfs(pdf_files, args.output)

if __name__ == "__main__":
    main()
