import requests
from bs4 import BeautifulSoup
import json
import os

# Ensure the output directory exists
output_dir = os.path.join(os.path.dirname(__file__), '../output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define the output file for storing indexed data
output_file = os.path.join(output_dir, 'index.json')

# Initialize the JSON file if it doesn't exist
if not os.path.exists(output_file):
    with open(output_file, 'w') as f:
        json.dump([], f)

def get_meta_tags(url):
    """Extract meta tags from a given URL"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the meta tags
        meta_tags = {}
        for tag in soup.find_all('meta'):
            if 'name' in tag.attrs:
                meta_tags[tag.attrs['name']] = tag.attrs.get('content', '')
            if 'property' in tag.attrs:
                meta_tags[tag.attrs['property']] = tag.attrs.get('content', '')
        
        return meta_tags
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_to_json(data):
    """Save the crawled data to the JSON file"""
    with open(output_file, 'r') as f:
        current_data = json.load(f)
    
    current_data.append(data)

    with open(output_file, 'w') as f:
        json.dump(current_data, f, indent=2)

def crawl_website(start_url):
    """Crawl the website, get pages, and store metadata"""
    visited_urls = set()
    urls_to_visit = [start_url]
    
    while urls_to_visit:
        url = urls_to_visit.pop(0)
        if url in visited_urls:
            continue
        
        visited_urls.add(url)
        print(f"Crawling: {url}")
        
        try:
            # Fetch the webpage
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save the meta tags and URL data
            meta_tags = get_meta_tags(url)
            if meta_tags:
                entity = {
                    'url': url,
                    'meta_tags': meta_tags
                }
                save_to_json(entity)
            
            # Find all links on the page and add them to the queue
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http'):
                    urls_to_visit.append(href)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

if __name__ == '__main__':
    # Ask for the start URL
    start_url = input("Enter the start URL: ")
    crawl_website(start_url)
