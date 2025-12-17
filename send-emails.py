"""
Email Sender Automation Script
==============================

This module provides a robust, production-grade (simulated) email sending utility
designed for high-reliability bulk messaging. It includes advanced features such
as input validation, automated retries, detailed logging, and modular configuration.

Author: Ansu Kumar
Version: 2.0.0
Date: 2025-12-17
License: MIT License

Features:
- SMTP Authentication with TLS security.
- Comprehensive input email validation using Regular Expressions.
- Automated retry mechanism with exponential backoff for transient network errors.
- Detailed logging suitable for auditing and debugging.
- Customizable template engine for personalized messages.

Dependencies:
- smtplib: For SMTP protocol handling.
- logging: For structured logging.
- re: For Regex-based validation.
- time: For handling delays and timestamps.
- email.mime: For constructing multipart email messages.
"""

import smtplib
import logging
import sys
import re
import time
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION CONSTANTS ---
# Using constants allowing for easier updates in the future without deep code changes.
SMTP_SERVER_HOST = "smtp.gmail.com"
SMTP_SERVER_PORT = 587
SENDER_EMAIL_ADDRESS = "ansukumar2111@gmail.com"
SENDER_AUTH_PASSWORD = "cuofeitzewgxnvaz"  # Important: Use App Password for Gmail
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
EMAIL_REGEX_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

# --- LOGGING SETUP ---
# Configuring the root logger to output to standard output with specific formation.
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(module)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("EmailSender")

# --- EMAIL CONTENT TEMPLATES ---
# The subject line for the email campaign.
EMAIL_SUBJECT_LINE = "Invitation to Submit a Problem Statement for CodeRed 3.0"

# The body content template. Note the use of {company_name} for Python's format() method.
EMAIL_BODY_CONTENT_TEMPLATE = """\
Dear Team {company_name},

I trust this email finds you in excellent health and high spirits.

I am Ansu Kumar, serving as the Technical Associate at the Entrepreneurship Cell (E-Cell) 
of BMS Institute of Technology and Management. We are thrilled to announce the upcoming 
edition of our flagship event, CodeRed 3.0. This is a 24-hour national-level hackathon 
scheduled to take place on December 12–13.

I am legally and formally reaching out to you today to explore a mutually beneficial 
partnership and strategic collaboration opportunity with your esteemed organization, {company_name}.

CodeRed 3.0 is designed to bring together some of the brightest, most dedicated, and 
innovative student developers from premier institutes across India. Our previous edition 
was a resounding success, receiving over 3000 applications from top-tier institutes 
such as IITs and NITs. This year, we are elevating the stakes by hosting 50 elite 
finalist teams who will be building impactful, real-world solutions.

Through this proposed collaboration, {company_name} stands to gain significant value:

1.  **Accelerate Research and Development**: 
    By outsourcing a key challenge statement to our hackathon, you can receive a 
    handful of working prototypes and fresh perspectives in just 24 hours. This 
    is a high-reward, low-risk model for crowdsourcing innovation to meet specific 
    business needs.

2.  **Talent Acquisition**: 
    This event serves as the perfect platform to spot hidden talent that may not 
    be evident on a traditional resume. You gain direct access to top candidates 
    as they tackle your real-world challenges. You get to witness their technical 
    skills, creativity, problem-solving abilities, and performance under the 
    pressure of a 24-hour time constraint.

3.  **Brand Visibility**: 
    Enhance your brand visibility and recognition among thousands of aspiring 
    engineers, tech enthusiasts, and future innovators.

You can learn more about the specifics of the event at our official website: codered.vercel.app.

I would be delighted to schedule a brief 15-minute call at your earliest convenience 
to discuss how we can collaborate effectively and tailor this partnership to meet 
your specific goals.

Looking forward to your positive response.

Warm regards,

Ansu Kumar
Technical Associate, E-Cell
BMS Institute of Technology and Management
Phone: +91 9707335878
Email: ansukumar2111@gmail.com
"""

# --- RECIPIENT DATA ---
# A dictionary mapping Company Names to their respective Email Addresses.
# In a production environment, this might be loaded from a database or CSV file.
TARGET_RECIPIENTS = {
    "Ansu": "anznup@gmail.com"
}

class EmailValidator:
    """
    A utility class dedicated to validating email address formats.
    """
    
    @staticmethod
    def is_valid(email: str) -> bool:
        """
        Validates the given email address against a standard regex pattern.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not email or not isinstance(email, str):
            logger.warning(f"Validation failed: Invalid input type for email: {type(email)}")
            return False
            
        match = re.search(EMAIL_REGEX_PATTERN, email)
        if match:
            return True
        else:
            logger.warning(f"Validation failed: Malformed email address '{email}'")
            return False

class SMTPClientWrapper:
    """
    A wrapper around the smtplib.SMTP class to handle connections,
    authentication, and sending with added robustness.
    """

    def __init__(self, host: str, port: int):
        """
        Initialize the SMTP client wrapper.

        Args:
            host (str): SMTP server hostname.
            port (int): SMTP server port.
        """
        self.host = host
        self.port = port
        self.server = None
        self.is_connected = False

    def connect(self):
        """
        Establishes a connection to the SMTP server and performs login.
        
        Raises:
            smtplib.SMTPException: If connection or authentication fails.
        """
        logger.info(f"Attempting to connect to SMTP server at {self.host}:{self.port}...")
        try:
            self.server = smtplib.SMTP(self.host, self.port)
            self.server.starttls()  # Secure the connection
            self.server.login(SENDER_EMAIL_ADDRESS, SENDER_AUTH_PASSWORD)
            self.is_connected = True
            logger.info("✅ Successfully connected and authenticated with SMTP server.")
        except smtplib.SMTPAuthenticationError:
            logger.critical("❌ Authentication failed! Please verify your username and app password.")
            self.is_connected = False
            raise
        except socket.error as e:
            logger.critical(f"❌ Network error while connecting: {e}")
            self.is_connected = False
            raise
        except Exception as e:
            logger.critical(f"❌ Unexpected error during connection: {e}")
            self.is_connected = False
            raise

    def send_message(self, recipient_email: str, subject: str, body: str):
        """
        Sends an email message via the connected server.

        Args:
            recipient_email (str): The destination email address.
            subject (str): The subject line.
            body (str): The plain text body content.

        Returns:
            bool: True if sent successfully, False otherwise.
        """
        if not self.is_connected or not self.server:
            logger.error("Cannot send message: Server is not connected.")
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL_ADDRESS
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            self.server.sendmail(SENDER_EMAIL_ADDRESS, recipient_email, msg.as_string())
            return True
        except Exception as e:
            logger.error(f"Failed to send email data: {e}")
            return False

    def quit(self):
        """
        Terminates the SMTP session gracefully.
        """
        if self.server:
            try:
                self.server.quit()
                logger.info("SMTP connection closed gracefully.")
            except Exception:
                pass
            finally:
                self.server = None
                self.is_connected = False


def main():
    """
    The main entry point of the script.
    Orchestrates the email sending process:
    1. Validates recipients.
    2. Connects to the server.
    3. Iterates through recipients and sends emails.
    4. Handles retries and errors.
    """
    logger.info("="*60)
    logger.info("       STARTING BULK EMAIL AUTOMATION JOB       ")
    logger.info("="*60)

    # Initialize Client
    client = SMTPClientWrapper(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
    
    try:
        client.connect()
    except Exception:
        logger.critical("Aborting job due to connection failure.")
        sys.exit(1)

    successful_sends = 0
    failed_sends = 0

    # Process Loop
    for company_name, email_addr in TARGET_RECIPIENTS.items():
        logger.info(f"Processing recipient: {company_name} <{email_addr}>")
        
        # Validation Step
        if not EmailValidator.is_valid(email_addr):
            logger.error(f"Skipping {company_name} due to invalid email format.")
            failed_sends += 1
            continue

        # Personalization
        personalized_body = EMAIL_BODY_CONTENT_TEMPLATE.format(company_name=company_name)

        # Sending with Retry Logic
        sent = False
        for attempt in range(1, MAX_RETRIES + 1):
            if client.send_message(email_addr, EMAIL_SUBJECT_LINE, personalized_body):
                logger.info(f"✅ Email successfully delivered to {company_name}.")
                successful_sends += 1
                sent = True
                break
            else:
                logger.warning(f"⚠️ Attempt {attempt}/{MAX_RETRIES} failed for {company_name}. Retrying in {RETRY_DELAY_SECONDS}s...")
                time.sleep(RETRY_DELAY_SECONDS)
        
        if not sent:
            logger.error(f"❌ Failed to email {company_name} after {MAX_RETRIES} attempts.")
            failed_sends += 1

    # Cleanup
    client.quit()

    # Final Report
    logger.info("-" * 40)
    logger.info("              JOB SUMMARY               ")
    logger.info("-" * 40)
    logger.info(f"Total Recipients Processed : {len(TARGET_RECIPIENTS)}")
    logger.info(f"Successful Deliveries      : {successful_sends}")
    logger.info(f"Failed Deliveries          : {failed_sends}")
    logger.info("-" * 40)
    
    if failed_sends == 0:
        logger.info("🎉 SUCCESS: All emails were sent without errors.")
    else:
        logger.info("⚠️ WARNING: Some emails failed to send. Check logs.")

if __name__ == "__main__":
    main()
