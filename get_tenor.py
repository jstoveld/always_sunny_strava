import requests
import random
from dotenv import load_dotenv
import os
load_dotenv()

TENOR_API_KEY = os.getenv("TENOR_API_KEY")

SEARCH_TERM = "always sunny"
LIMIT = 20  # Number of gifs to fetch per request

def get_random_sunny_gif():
    url = f"https://tenor.googleapis.com/v2/search"
    params = {
        "q": SEARCH_TERM,
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

gif_url = get_random_sunny_gif()
if gif_url:
    filename = download_gif(gif_url)
    print(f"downloaded gif to {filename}")
else:
    print(f"No gif found.")