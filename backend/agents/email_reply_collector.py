from email.header import decode_header
import imaplib
import email
import os
import pandas as pd
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding='utf-8')


load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Load sent leads to filter replies
try:
    leads_df = pd.read_csv("data/leads_enriched.csv")
    sent_emails = set()
    for row in leads_df["emails"].dropna():
        sent_emails.update([e.strip() for e in row.split(",")])
except Exception as e:
    print(f"[!] Failed to load sent emails: {e}")
    sent_emails = set()

def clean_subject(raw_subject):
    decoded = decode_header(raw_subject)
    subject = ""
    for part, enc in decoded:
        if isinstance(part, bytes):
            subject += part.decode(enc or "utf-8", errors="ignore")
        else:
            subject += part
    return subject.strip()

def fetch_real_replies():
    print("[*] Connecting to Gmail...")
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("[!] Email credentials not set. Skipping reply checks.")
        return

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("[✓] Logged in")
    except Exception as e:
        print(f"[!] IMAP login failed: {e}")
        return

    mail.select("inbox")
    status, messages = mail.search(None, '(UNSEEN SUBJECT "Re:")')
    if status != "OK":
        print("[!] Search failed")
        return

    msg_ids = messages[0].split()[:50]
    print(f"[✓] Found {len(msg_ids)} candidate replies")

    real_replies = []

    for num in msg_ids:
        res, msg_data = mail.fetch(num, "(RFC822)")
        if res != "OK":
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                from_ = email.utils.parseaddr(msg["From"])[1]

                # Filter automated systems
                if "@facebookmail.com" in from_ or from_ not in sent_emails:
                    continue

                subject = clean_subject(msg["Subject"])

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                real_replies.append({
                    "from": from_,
                    "subject": subject,
                    "body": body.strip()
                })

    if real_replies:
        df = pd.DataFrame(real_replies)
        df.to_csv("data/replies_filtered.csv", index=False)
        print(f"[✓] Saved {len(real_replies)} real replies to data/replies_filtered.csv")
    else:
        print("[*] No real replies found.")

if __name__ == "__main__":
    fetch_real_replies()
