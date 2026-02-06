import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.search import search_duckduckgo
from core.utils import save_leads_to_csv

import sys
sys.stdout.reconfigure(encoding='utf-8')



def collect_leads(search_term):
    print(f"[+] Searching for: {search_term}")
    results = search_duckduckgo(search_term, max_results=20)

    leads = []
    for r in results:
        print(f" - {r['title']}")
        leads.append({
            "name": r["title"],
            "url": r["url"],
            "snippet": r["snippet"]
        })

    save_leads_to_csv(leads)
    print(f"[✓] Saved {len(leads)} leads to data/leads_raw.csv")
    return len(leads)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        collect_leads(query)
    else:
        # Optional fallback if someone runs the script standalone
        query = input("Enter search term (e.g., SaaS companies in Europe): ")
        collect_leads(query)
