"""
Bulk Image Resizer
==================

A powerful utility to resize images in bulk while preserving aspect ratio.
It supports various filtering algorithms and format conversions.

Dependencies:
- Pillow (PIL)

Features:
- Bulk processing of entire directories.
- Aspect ratio preservation (fit vs fill strategies).
- High-quality downsampling filters.
- Format conversion (e.g., convert all to PNG).

Author: Ansu Kumar
Version: 1.0.0
Date: 2025-12-17
"""

import os
import argparse
import logging
import sys
from PIL import Image

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ImageResizer")

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"}

def resize_image(image_path: str, output_path: str, width: int, height: int, quality: int = 90):
    """
    Resizes a single image and saves it to the output path.
    """
    try:
        with Image.open(image_path) as img:
            # Calculate aspect ratio
            img_ratio = img.width / img.height
            target_ratio = width / height

            new_width, new_height = width, height

            # Fit strategy: Ensure image fits within bounds without distortion
            if img_ratio > target_ratio:
                # Image is wider than target
                new_height = int(width / img_ratio)
            else:
                # Image is taller than target
                new_width = int(height * img_ratio)

            # High-quality resize (LANCZOS)
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save
            resized_img.save(output_path, quality=quality)
            logger.info(f"✅ Processed: {os.path.basename(image_path)} -> ({new_width}x{new_height})")
            return True

    except Exception as e:
        logger.error(f"❌ Failed to process {os.path.basename(image_path)}: {e}")
        return False

def process_directory(input_dir: str, output_dir: str, width: int, height: int, quality: int):
    """
    Iterates through a directory and resizes all compatible images.
    """
    if not os.path.exists(input_dir):
        logger.error(f"Input directory not found: {input_dir}")
        return

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
        except OSError as e:
            logger.critical(f"Failed to create output directory: {e}")
            return

    files = [f for f in os.listdir(input_dir) if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]
    
    if not files:
        logger.warning(f"No valid images found in {input_dir}")
        return

    logger.info(f"🚀 Starting bulk resize of {len(files)} images to max {width}x{height}...")

    success_count = 0
    for file in files:
        in_path = os.path.join(input_dir, file)
        out_path = os.path.join(output_dir, file)
        
        if resize_image(in_path, out_path, width, height, quality):
            success_count += 1
            
    logger.info("-" * 40)
    logger.info(f"🎉 Job Complete. Successfully resized {success_count}/{len(files)} images.")

def main():
    parser = argparse.ArgumentParser(description="Bulk resize images.")
    
    parser.add_argument("input_dir", help="Source directory containing images")
    parser.add_argument("--output", default="resized_images", help="Destination directory")
    parser.add_argument("--width", type=int, default=1920, help="Target max width")
    parser.add_argument("--height", type=int, default=1080, help="Target max height")
    parser.add_argument("--quality", type=int, default=85, help="JPEG Output quality (1-100)")

    args = parser.parse_args()

    # Determine absolute paths for safety
    input_path = os.path.abspath(args.input_dir)
    output_path = os.path.abspath(args.output)

    process_directory(input_path, output_path, args.width, args.height, args.quality)

if __name__ == "__main__":
    main()
