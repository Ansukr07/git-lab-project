"""
Certificate Generation Module
=============================

This module facilitates the automated generation of digital certificates for events,
workshops, and hackathons. It processes a list of names, usually provided via a CSV
file, and overlays them onto a pre-designed certificate template image.

It employs the Python Imaging Library (PIL/Pillow) for high-quality image manipulation
and text rendering.

Author: Ansu Kumar
Version: 2.1.0
Date: 2025-12-17
"""

import os
import csv
import argparse
import logging
import sys
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageColor

# --- CONFIGURATION DEFAULTS ---
DEFAULT_TEMPLATE = "certificate_template.png"
DEFAULT_OUTPUT_DIR = "generated_certificates"
DEFAULT_FONT_PATH = "arial.ttf"
DEFAULT_FONT_SIZE = 60
DEFAULT_COORDINATES = (960, 540)  # Center (X, Y)
DEFAULT_TEXT_COLOR = "black"

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("CertificateGen")

class CertificateGenerator:
    """
    A class to handle the configuration and state of the certificate generation process.
    """

    def __init__(self, template_path: str, output_dir: str, font_path: str, font_size: int, text_color: str, position: Tuple[int, int]):
        """
        Initialize the generator with path configurations and design properties.

        Args:
            template_path (str): Path to the base certificate image.
            output_dir (str): Directory where generated images will be saved.
            font_path (str): Path to the TrueType font file.
            font_size (int): Size of the font in points.
            text_color (str): Color name or hex code for the text.
            position (Tuple[int, int]): (x, y) coordinates for the text center.
        """
        self.template_path = template_path
        self.output_dir = output_dir
        self.font_path = font_path
        self.font_size = font_size
        self.raw_text_color = text_color
        self.position = position

        self.font = None
        self.parsed_color = None
        
        self.validate_paths()
        self.load_resources()

    def validate_paths(self):
        """Validates input paths and creates output directory."""
        if not os.path.exists(self.template_path):
            logger.error(f"❌ Template file not found: {self.template_path}")
            sys.exit(1)
        
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
                logger.info(f"📂 Created output directory: {self.output_dir}")
            except OSError as e:
                logger.critical(f"❌ Failed to create output directory: {e}")
                sys.exit(1)

    def load_resources(self):
        """Loads the font and parses the color."""
        # Load Font
        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
            logger.info(f"✅ Loaded font: {self.font_path} (Size: {self.font_size})")
        except IOError:
            logger.warning(f"⚠️ Font '{self.font_path}' not found. Using system default.")
            self.font = ImageFont.load_default()

        # Parse Color
        try:
            self.parsed_color = ImageColor.getrgb(self.raw_text_color)
            logger.info(f"🎨 Text color set to: {self.raw_text_color} {self.parsed_color}")
        except ValueError:
            logger.warning(f"⚠️ Invalid color '{self.raw_text_color}'. Defaulting to black.")
            self.parsed_color = (0, 0, 0)

    def generate_single(self, name: str) -> bool:
        """
        Generates a single certificate for the given name.

        Args:
            name (str): The name to print on the certificate.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            image = Image.open(self.template_path)
            draw = ImageDraw.Draw(image)

            # Center Text Logic
            # Note: textbbox is the modern replacement for textsize in newer Pillow versions
            text_bbox = draw.textbbox((0, 0), name, font=self.font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = self.position[0] - (text_width / 2)
            y = self.position[1] - (text_height / 2)

            # Draw the text
            draw.text((x, y), name, fill=self.parsed_color, font=self.font)

            # Save
            filename = f"{name.replace(' ', '_')}.png"
            full_path = os.path.join(self.output_dir, filename)
            image.save(full_path)
            return True

        except Exception as e:
            logger.error(f"failed to generate for '{name}': {e}")
            return False

    def process_csv(self, csv_file_path: str):
        """
        Reads names from a CSV and runs the generation loop.
        """
        if not os.path.exists(csv_file_path):
            logger.error(f"❌ CSV file not found: {csv_file_path}")
            return

        logger.info(f"🚀 Processing batch from: {csv_file_path}")
        
        count = 0
        success = 0
        
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                
                # Assume name is the first column
                name = row[0].strip()
                if not name:
                    continue

                if self.generate_single(name):
                    logger.info(f"  [+] Generated certificate for: {name}")
                    success += 1
                else:
                    logger.error(f"  [-] Failed to generate for: {name}")
                count += 1

        logger.info("-" * 40)
        logger.info(f"Batch completed. Total: {count}, Success: {success}, Errors: {count - success}")


def create_dummy_csv_if_needed(csv_path: str):
    """Helper to create a CSV for testing purposes."""
    if not os.path.exists(csv_path) and csv_path == "names.csv":
        logger.info("ℹ️ Creating dummy 'names.csv' for testing.")
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([["Alice Johnson"], ["Bob Smothers"], ["Charlie Day"]])

def main():
    """Main CLI Entry Point."""
    parser = argparse.ArgumentParser(
        description="Bulk generate event certificates from a CSV list.",
        epilog="Example: python generate_certificates.py names.csv --color '#FF5733'"
    )
    
    parser.add_argument("csv_file", nargs="?", default="names.csv", help="Input CSV file with names")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE, help="Template image path")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--font", default=DEFAULT_FONT_PATH, help="Font file path")
    parser.add_argument("--size", type=int, default=DEFAULT_FONT_SIZE, help="Font size")
    parser.add_argument("--color", default=DEFAULT_TEXT_COLOR, help="Text color (name or hex)")
    parser.add_argument("--x", type=int, default=DEFAULT_COORDINATES[0], help="X coordinate center")
    parser.add_argument("--y", type=int, default=DEFAULT_COORDINATES[1], help="Y coordinate center")

    args = parser.parse_args()

    # Pre-check CSV for better user experience
    create_dummy_csv_if_needed(args.csv_file)

    # Instantiate Generator
    generator = CertificateGenerator(
        template_path=args.template,
        output_dir=args.output,
        font_path=args.font,
        font_size=args.size,
        text_color=args.color,
        position=(args.x, args.y)
    )

    # Run Process
    generator.process_csv(args.csv_file)

if __name__ == "__main__":
    main()
