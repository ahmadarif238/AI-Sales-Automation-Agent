from ddgs import DDGS
import json

def test_search():
    query = "Marketing agencies in New York"
    print(f"Testing search for: '{query}'")
    
    try:
        results = []
        with DDGS() as ddgs:
            # Try getting just 5 results
            gen = ddgs.text(query, max_results=5)
            if gen:
                for r in gen:
                    results.append(r)
        
        print(f"Found {len(results)} results.")
        if results:
            print("First result:", results[0])
        else:
            print("No results returned from DDGS.")
            
    except Exception as e:
        print(f"Error during search: {e}")

if __name__ == "__main__":
    test_search()
