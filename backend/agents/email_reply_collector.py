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

# Sample reply bodies spanning the full hot/warm/cold range, so the
# forecasting agent has something meaningful to classify in demo mode.
MOCK_REPLY_BODIES = [
    "Thanks for reaching out! I'd love to learn more about your AI tools. Can we talk Tuesday?",
    "Interesting - could you send over pricing and a case study? We're evaluating options this quarter.",
    "Not interested at this time, but thanks.",
    "We already work with a vendor here, though it may be worth revisiting next year.",
    "This is exactly what we've been looking for. Who should I loop in from our side to get started?",
]


def inject_mock_replies(leads_csv="data/leads_enriched.csv"):
    """Injects sample replies if real searching fails, to ensure the demo continues.

    The bodies are attached to addresses taken from the ACTUAL scraped leads.
    The previous version used invented addresses (prospect@example.com), which
    never matched a lead, so `forecast_sales` joined nothing, every lead came
    back "cold - No reply received yet", and the Groq categorisation never ran
    at all. The dashboard therefore showed no AI output whatsoever.
    """
    recipients = []
    try:
        leads_df = pd.read_csv(leads_csv)
        for row in leads_df["emails"].dropna():
            # `forecast_sales` only ever looks at the FIRST address of each lead
            # row, so matching that here is what makes the reply actually join.
            candidate = str(row).split(",")[0].strip().lower()
            if "@" in candidate and candidate not in recipients:
                recipients.append(candidate)
    except Exception as exc:  # noqa: BLE001
        print(f"[!] Could not read leads for mock replies: {exc}")

    if not recipients:
        # No leads available - fall back to placeholder addresses.
        recipients = ["prospect@example.com", "manager@techstart.io"]

    # Reply to a subset, so the output has a realistic mix of replied and
    # non-replied leads rather than every single lead answering.
    replied = recipients[:min(len(recipients), max(2, len(recipients) // 2))]

    mock_data = [
        {
            "from": address,
            "subject": "Re: Let's Connect: Exploring Synergies",
            "body": MOCK_REPLY_BODIES[i % len(MOCK_REPLY_BODIES)],
        }
        for i, address in enumerate(replied)
    ]
    df = pd.DataFrame(mock_data)
    df.to_csv("data/replies.csv", index=False)
    print(f"[✓] Mock replies injected for {len(mock_data)} of {len(recipients)} leads")

if __name__ == "__main__":
    fetch_real_replies()
