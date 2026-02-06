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

# Simple regex to validate email (moved up)
def is_valid_email(email):
    if not isinstance(email, str): return False
    if email.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def send_email(to_email, subject, body):
    if not EMAIL or not PASSWORD:
        print(f"[*] [MOCK] Sending email to {to_email}...")
        time.sleep(0.5) # Small delay for realism
        print(f"[✓] [MOCK] Email sent to {to_email}")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    try:
        # Reduced timeout for faster failure
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print(f"[✓] Sent email to {to_email}")
    except Exception as e:
        print(f"[!] Failed to send to {to_email}: {e}")
        print(f"[*] [FALLBACK] Simulating send for demo stability...")

import time

def engage_leads(csv_path="data/leads_scored.csv", min_score=1):
    if not os.path.exists(csv_path):
        print(f"[!] {csv_path} not found. Skipping engagement.")
        return

    df = pd.read_csv(csv_path)
    sent_emails = set()

    print(f"[*] Starting engagement for high-scoring leads...")
    
    for _, row in df.iterrows():
        score = row.get("score", 0)
        emails_raw = row.get("emails")
        
        if score >= min_score and pd.notna(emails_raw):
            for email in str(emails_raw).split(","):
                clean_email = email.strip()
                if is_valid_email(clean_email) and clean_email not in sent_emails:
                    send_email(clean_email, EMAIL_SUBJECT, EMAIL_BODY_TEMPLATE)
                    sent_emails.add(clean_email)

if __name__ == "__main__":
    engage_leads()
