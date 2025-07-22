from fastapi import FastAPI
from modules.scraper import fetch_football365_headlines, save_headlines_to_file

app = FastAPI()

@app.get("/scrape-headlines")
def scrape_headlines():
    headlines = fetch_football365_headlines()
    if not headlines:
        return {"success": False, "message": "No headlines found."}
    save_headlines_to_file(headlines)
    return {"success": True, "count": len(headlines), "message": "Headlines scraped and saved."}