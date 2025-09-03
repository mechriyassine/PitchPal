import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.rag import query_headlines

# Sample test cases: (query, expected keyword in headline)
test_cases = [
    ("Liverpool", "Liverpool"),
    ("Arsenal", "Arsenal"),
    ("Man Utd", "Man Utd"),
    ("Marc Guehi", "Guehi"),
    ("Ballon d’Or", "Ballon d’Or"),
]

def test_retrieval():
    for query, expected in test_cases:
        results = query_headlines(query)
        found = any(expected.lower() in h.lower() for h in results)
        print(f"Query: {query} | Expected: {expected} | Found: {found}")
        if not found:
            print("  Retrieved headlines:", results)

if __name__ == "__main__":
    test_retrieval()