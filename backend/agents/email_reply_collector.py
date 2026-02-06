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
    print("[*] Checking for replies...")
    
    # Check for credentials
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("[!] Email credentials not set. Injecting mock replies for demo...")
        inject_mock_replies()
        return

    try:
        # Reduced timeout
        mail = imaplib.IMAP4_SSL("imap.gmail.com", timeout=10)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("[✓] Logged in to Gmail")
        
        mail.select("inbox")
        status, messages = mail.search(None, '(UNSEEN SUBJECT "Re:")')
        if status != "OK":
            print("[!] Search failed")
            inject_mock_replies()
            return

        msg_ids = messages[0].split()[:50]
        print(f"[✓] Found {len(msg_ids)} candidate replies")

        real_replies = []
        for num in msg_ids:
            res, msg_data = mail.fetch(num, "(RFC822)")
            if res != "OK": continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    from_ = email.utils.parseaddr(msg["From"])[1]
                    if from_ not in sent_emails: continue

                    subject = clean_subject(msg["Subject"])
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    real_replies.append({"from": from_, "subject": subject, "body": body.strip()})

        if real_replies:
            df = pd.DataFrame(real_replies)
            df.to_csv("data/replies.csv", index=False)
            print(f"[✓] Saved {len(real_replies)} real replies")
        else:
            print("[*] No real replies found. Injecting mock data...")
            inject_mock_replies()

    except Exception as e:
        print(f"[!] IMAP Error: {e}")
        print("[*] Using mock replies for demo stability...")
        inject_mock_replies()

def inject_mock_replies():
    """Injects sample replies if real searching fails, to ensure the demo continues."""
    mock_data = [
        {"from": "prospect@example.com", "subject": "Re: Let's Connect", "body": "Thanks for reaching out! I'd love to learn more about your AI tools. Can we talk Tuesday?"},
        {"from": "manager@techstart.io", "subject": "Re: Exploring Synergies", "body": "Not interested at this time, but thanks."}
    ]
    df = pd.DataFrame(mock_data)
    df.to_csv("data/replies.csv", index=False)
    print("[✓] Mock replies injected into data/replies.csv")

if __name__ == "__main__":
    fetch_real_replies()
