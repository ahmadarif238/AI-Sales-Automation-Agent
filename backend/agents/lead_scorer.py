import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')


def score_email(email_str):
    if pd.isna(email_str) or email_str.strip() == "" or email_str == "N/A":
        return 0
    emails = str(email_str).split(", ")
    score = 0
    for email in emails:
        email = email.lower()
        if "@gmail.com" in email or "@outlook.com" in email:
            score += 1
        elif "info@" in email or "admin@" in email:
            score += 2
        else:
            score += 3  # likely personal or company email
    return min(score, 10)

def score_leads(in_csv="data/leads_enriched.csv", out_csv="data/leads_scored.csv"):
    df = pd.read_csv(in_csv)
    df["emails"] = df["emails"].fillna("")  # handle NaN safely
    df["score"] = df["emails"].apply(score_email)
    df = df.sort_values(by="score", ascending=False)
    df.to_csv(out_csv, index=False)
    print(f"[✓] Scored {len(df)} leads and saved to {out_csv}")

if __name__ == "__main__":
    score_leads()
