import requests
from bs4 import BeautifulSoup
import random
from dotenv import load_dotenv
import os

load_dotenv()
TENOR_API_KEY = os.getenv("TENOR_API_KEY")
LIMIT = 20  # Number of gifs to fetch per request

USED_QUOTES_FILE = "used_quotes.txt"

def fetch_imdb_quotes():
    url = "https://www.imdb.com/title/tt0472954/quotes/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    for li in soup.select("div.ipc-html-content-inner-div ul li"):
        text = li.get_text(separator=" ", strip=True)
        # Remove character names (everything before the first colon)
        lines = []
        for line in text.split('\n'):
            if ":" in line and len(line) > 20:
                quote_only = line.split(":", 1)[1].strip()
                if len(quote_only) > 10:
                    lines.append(quote_only)
        if lines:
            quotes.extend(lines)
        elif len(text) > 20 and ":" not in text:
            quotes.append(text)
    return quotes

def get_unused_quote(quotes):
    if os.path.exists(USED_QUOTES_FILE):
        with open(USED_QUOTES_FILE, "r") as f:
            used = set(line.strip() for line in f)
    else:
        used = set()
    unused = [q for q in quotes if q not in used]
    if not unused:
        with open(USED_QUOTES_FILE, "w") as f:
            pass
        unused = quotes[:]
    quote = random.choice(unused)
    with open(USED_QUOTES_FILE, "a") as f:
        f.write(quote + "\n")
    return quote

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
    quotes = fetch_imdb_quotes()
    if quotes:
        search_term = get_unused_quote(quotes)
        gif_url = get_random_sunny_gif(search_term)
        if gif_url:
            filename = download_gif(gif_url)
            print(f"Downloaded gif to {filename} using search term: '{search_term}'")
        else:
            print(f"No gif found for search term: '{search_term}'")
    else:
        print("No quotes found.")