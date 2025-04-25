import requests
from bs4 import BeautifulSoup
from .indexer import save_to_json
from .utils import clean_url

# Function to start crawling
def crawl(url, max_depth=3, depth=1, visited=set()):
    if depth > max_depth:
        return

    # Avoid revisiting pages
    if url in visited:
        return
    visited.add(url)

    print(f"Crawling: {url}")

    # Request the page and parse it
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error requesting {url}: {e}")
        return

    # Extract all the links in the page
    links = soup.find_all('a', href=True)
    for link in links:
        link_url = clean_url(link['href'], base_url=url)
        save_to_json(link_url)  # Save link to json
        crawl(link_url, max_depth, depth + 1, visited)

# Start crawling from a given URL
if __name__ == "__main__":
    start_url = "https://example.com"
    crawl(start_url)