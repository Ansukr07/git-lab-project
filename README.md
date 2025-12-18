# Automation Scripts Project

This repository contains a suite of python scripts designed to automate common administrative and file management tasks.

## 🚀 Scripts

*Last Updated for Submission*


### 1. `send-emails.py` - Automated Email Sender
A robust script to send personalized bulk emails using SMTP (Gmail).

- **Features**: 
  - Personalization placeholders (`{company_name}`).
  - Logging of success/failure.
  - Exception handling for robust execution.
- **Config**: Edit `SENDER_EMAIL` and `SENDER_PASSWORD` in the script.

### 2. `generate_certificates.py` - Certificate Generator
Generates certificates from a template and a list of names.

- **Features**:
  - Automatically center text.
  - Supports custom fonts.
  - CLI support.
- **Usage**:
  ```bash
  python generate_certificates.py [names.csv] --template template.png --output ./certs
  ```

### 3. `organize_files.py` - Smart File Organizer
 cleans up cluttered directories by sorting files into categorized folders.

- **Categories**: Images, Documents, Videos, Music, Archives, Scripts, Executables.
- **Usage**:
  ```bash
  python organize_files.py [directory]
  
  # Dry Run (Safe Mode)
  python organize_files.py --dry-run
  ```

### 4. `utils.py` - Shared Helpers
Common utility functions for logging and file management used across the project.

## 📦 Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🛠️ Contribution
1. Fork the repo.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch. 
