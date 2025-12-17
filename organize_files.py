import os
import shutil

# --- CONFIGURATION ---
DIRECTORY_TO_ORGANIZE = "."  # Current directory
EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".sh", ".bat"]
}

def organize_files():
    for filename in os.listdir(DIRECTORY_TO_ORGANIZE):
        try:
            filepath = os.path.join(DIRECTORY_TO_ORGANIZE, filename)

            # Skip directories and this script itself
            if os.path.isdir(filepath) or filename == os.path.basename(__file__):
                continue
            
            # Find the category
            _, ext = os.path.splitext(filename)
            category = "Others" # Default
            
            for cat, exts in EXTENSIONS.items():
                if ext.lower() in exts:
                    category = cat
                    break
            
            # Create category folder if it doesn't exist
            category_path = os.path.join(DIRECTORY_TO_ORGANIZE, category)
            if not os.path.exists(category_path):
                os.makedirs(category_path)

            # Move file
            shutil.move(filepath, os.path.join(category_path, filename))
            print(f"Moved: {filename} -> {category}/")

        except Exception as e:
            print(f"❌ Error moving {filename}: {e}")

if __name__ == "__main__":
    print(f"Cleaning up directory: {os.path.abspath(DIRECTORY_TO_ORGANIZE)} ...")
    confirmation = input("Are you sure? (y/n): ")
    if confirmation.lower() == 'y':
        organize_files()
        print("✅ Cleanup complete.")
    else:
        print("❌ Operation cancelled.")
