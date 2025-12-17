import os
import csv
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
TEMPLATE_PATH = "certificate_template.png"
OUTPUT_FOLDER = "generated_certificates"
FONT_PATH = "arial.ttf"  # Ensure this font exists or use a system path
FONT_SIZE = 60
TEXT_COLOR = (0, 0, 0)
COORDINATES = (960, 540) # (x, y) - Center of the text roughly

def generate_certificates(csv_file):
    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Check if template exists
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ Error: Template '{TEMPLATE_PATH}' not found. Please add a template image.")
        return

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"⚠️ Warning: Font '{FONT_PATH}' not found. Falling back to default font.")
        font = ImageFont.load_default()

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        # Assuming CSV has no header or just names. If header, skip it: next(reader)
        
        for row in reader:
            if not row: continue
            name = row[0].strip()
            
            image = Image.open(TEMPLATE_PATH)
            draw = ImageDraw.Draw(image)

            # Calculate text width to center it
            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = COORDINATES[0] - (text_width / 2)
            y = COORDINATES[1] - (text_height / 2)

            draw.text((x, y), name, fill=TEXT_COLOR, font=font)

            output_path = os.path.join(OUTPUT_FOLDER, f"{name}.png")
            image.save(output_path)
            print(f"✅ Certificate generated for: {name}")

    print("🎉 All certificates generated!")

if __name__ == "__main__":
    # Create a dummy CSV if it doesn't exist for testing
    if not os.path.exists("names.csv"):
        with open("names.csv", "w") as f:
            f.write("Alice Smith\nBob Jones\nCharlie Brown")
        print("ℹ️ Created dummy 'names.csv'.")

    generate_certificates("names.csv")
