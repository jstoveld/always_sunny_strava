import requests
from bs4 import BeautifulSoup
import random
from dotenv import load_dotenv
import os

load_dotenv()
TENOR_API_KEY = os.getenv("TENOR_API_KEY")
LIMIT = 20  # Number of gifs to fetch per request

def get_season_links():
    url = "https://en.wikiquote.org/wiki/It%27s_Always_Sunny_in_Philadelphia"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    season_links = []
    for a in soup.select('a[href^="/wiki/It%27s_Always_Sunny_in_Philadelphia_(season_"]'):
        season_links.append("https://en.wikiquote.org" + a['href'])
    return season_links

def fetch_sunny_quotes(season_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(season_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    # Find all <ul> elements that are not part of navigation or references
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            text = li.get_text(strip=True)
            # Filter out episode titles and short lines
            if len(text) > 20 and not text.startswith("Retrieved") and not text.startswith("See also"):
                quotes.append(text)
    return quotes

def get_random_sunny_gif(search_term):
    url = f"https://tenor.googleapis.com/v2/search"
    params = {
        "q": search_term,
        "key": TENOR_API_KEY,
        "limit": LIMIT,
        "media_filter": "minimal"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        return None
    gif = random.choice(results)
    return gif["media_formats"]["gif"]["url"]

def download_gif(gif_url, filename="sunny.gif"):
    response = requests.get(gif_url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename

if __name__ == "__main__":
    season_links = get_season_links()
    if season_links:
        season_url = random.choice(season_links)
        quotes = fetch_sunny_quotes(season_url)
        if quotes:
            search_term = random.choice(quotes)
            gif_url = get_random_sunny_gif(search_term)
            if gif_url:
                filename = download_gif(gif_url)
                print(f"Downloaded gif to {filename} using search term: '{search_term}'")
            else:
                print(f"No gif found for search term: '{search_term}'")
        else:
            print("No quotes found in season.")
    else:
        print("No season links found.")