# Email Sender Script

This Python script (`send-emails.py`) allows you to send personalized bulk emails using an SMTP server (defaulted to Gmail).

## Features
- Sends emails via SMTP.
- Personalizes the email body with the recipient's company name/name.
- Handles multiple recipients from a dictionary.

## Prerequisites
- Python 3.x installed.
- A Gmail account (or another email provider with SMTP access).
- An **App Password** if using Gmail (since less secure apps are no longer supported).

## Configuration

1.  **Sender Credentials**:
    Open `send-emails.py` and update the following variables:
    ```python
    SENDER_EMAIL = "your-email@gmail.com"
    SENDER_PASSWORD = "your-app-password"
    ```
    > **⚠️ Security Warning**: It is not recommended to hardcode passwords in scripts, especially if pushing to a public repository. Consider using environment variables or a separate config file.

2.  **Recipients List**:
    Update the `recipients` dictionary in the script:
    ```python
    recipients = {
        "Company Name 1": "email1@example.com",
        "Company Name 2": "email2@example.com"
    }
    ```
    The key is used to personalize the email (e.g., "Dear Team {Company Name 1}"), and the value is the destination email address.

3.  **Email Content**:
    Modify the `subject` and `body` variables to customize your message. ensure `{company_name}` remains in the body string for the personalization logic to work, or remove the `.format()` call in the sending loop if you don't need it.

## Usage

Run the script from your terminal:

```bash
python send-emails.py
```

## Troubleshooting
- **Authentication Error**: Ensure you are using an App Password, not your login password.
- **Connection Issues**: Check your internet connection and firewall settings. Ensure port 587 is allowed.
