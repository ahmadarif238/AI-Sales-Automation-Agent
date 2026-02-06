import pandas as pd
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Load credentials
load_dotenv()
EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

# Email Template
EMAIL_SUBJECT = "Let's Connect: Exploring Synergies"
EMAIL_BODY_TEMPLATE = """
Hi,

I came across your work and thought it would be valuable to connect. We're helping B2B companies like yours with AI-driven sales solutions that save time and boost conversions.

Would love to chat briefly and see if there's alignment.

Best,  
Arif  
"""

# Simple regex to validate email
def is_valid_email(email):
    # Reject clearly invalid patterns (like .png, .jpg, etc.)
    if email.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
        return False

    # Basic email regex
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    if not EMAIL or not PASSWORD:
        print(f"[!] Email credentials not set. Skipping email to {to_email}")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print(f"[✓] Sent email to {to_email}")
    except Exception as e:
        print(f"[!] Failed to send to {to_email}: {e}")

def engage_leads(csv_path="data/leads_scored.csv", min_score=1):
    df = pd.read_csv(csv_path)
    sent_emails = set()

    for _, row in df.iterrows():
        if row.get("score", 0) >= min_score and pd.notna(row.get("emails")):
            for email in str(row["emails"]).split(","):
                clean_email = email.strip()
                if is_valid_email(clean_email) and clean_email not in sent_emails:
                    send_email(clean_email, EMAIL_SUBJECT, EMAIL_BODY_TEMPLATE)
                    sent_emails.add(clean_email)

if __name__ == "__main__":
    engage_leads()
