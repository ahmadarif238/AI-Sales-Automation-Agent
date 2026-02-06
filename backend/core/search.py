from ddgs import DDGS

def search_duckduckgo(query, max_results=10):
    results = []
    with DDGS() as ddgs:
        # Use a try-except block to handle potential API changes or network issues
        try:
            results_gen = ddgs.text(query, max_results=max_results)
            if results_gen:
                for r in results_gen:
                    results.append({
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": r.get("body")
                    })
        except Exception as e:
            print(f"Search error: {e}")
    return results
