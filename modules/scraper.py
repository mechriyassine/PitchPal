import requests
from bs4 import BeautifulSoup

def fetch_football365_headlines():
    url = "https://www.football365.com/news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []

    h3_tags = soup.find_all("h3")
    print(f"Found {len(h3_tags)} <h3> tags")

    for h3 in h3_tags:
        text = h3.get_text(strip=True)
        if text and text not in headlines:
            headlines.append(text)
    return headlines

def save_headlines_to_file(headlines, filename="headlines.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for idx, headline in enumerate(headlines, 1):
            f.write(f"{idx}. {headline}\n")
    print(f"Saved {len(headlines)} headlines to {filename}")

if __name__ == "__main__":
    headlines = fetch_football365_headlines()
    if not headlines:
        print("No headlines found. The page structure may have changed.")
    else:
        save_headlines_to_file(headlines)