import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
from core.utils import extract_emails
import sys
sys.stdout.reconfigure(encoding='utf-8')


import concurrent.futures

COMMON_PATHS = ["", "contact", "about", "team"]

def enrich_url(base_url):
    enriched = {"url": base_url, "emails": "N/A"}
    emails = set()
    
    # Check main page fast
    try:
        print(f"[*] Checking: {base_url}")
        res = requests.get(base_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code == 200:
            emails.update(extract_emails(res.text))
    except:
        pass

    # Check other paths only if needed or concurrently (simplified here to just 1 path to save time if we found emails)
    # For speed, let's checking just 'contact' if main page yielded nothing, or check all quickly.
    
    for path in ["contact"]:  # Reduced paths for speed
        if len(emails) > 0: break # Stop if we found emails
        try:
            full_url = urljoin(base_url, path)
            res = requests.get(full_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code == 200:
                emails.update(extract_emails(res.text))
        except:
            continue

    enriched["emails"] = ", ".join(emails) if emails else "N/A"
    return enriched

def enrich_all(raw_csv="data/leads_raw.csv", out_csv="data/leads_enriched.csv"):
    df = pd.read_csv(raw_csv)
    enriched_data = []

    print(f"[*] Starting enrichment for {len(df)} leads...")
    
    # Process leads in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {}
        for idx, row in df.iterrows():
            url = row.get("url") or row.get("link")
            if isinstance(url, str) and url.startswith("http"):
                 future = executor.submit(enrich_url, url)
                 future_to_url[future] = url
        
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
                if data:
                    enriched_data.append(data)
            except Exception as exc:
                print(f"[!] Analysis failed: {exc}")

    pd.DataFrame(enriched_data).to_csv(out_csv, index=False)
    print(f"\n[✓] Enriched {len(enriched_data)} leads saved to {out_csv}")

if __name__ == "__main__":
    enrich_all()
