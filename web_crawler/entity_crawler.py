import json
import requests
from bs4 import BeautifulSoup

# List of Schema.org types to extract
VALID_TYPES = ["Person", "Organization", "Product", "Event", "Place", "Article", "SoftwareApplication"]

def extract_json_ld_entities(url):
    """Fetch a URL and extract valid JSON-LD entities."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', type='application/ld+json')
        found_entities = []

        for script in script_tags:
            if not script.string:
                continue
            try:
                raw_json = json.loads(script.string)
                # Ensure it's always a list
                json_list = raw_json if isinstance(raw_json, list) else [raw_json]

                for entity in json_list:
                    if isinstance(entity, dict) and entity.get('@type') in VALID_TYPES:
                        found_entities.append({
                            "url": url,
                            "entity": entity
                        })
            except json.JSONDecodeError:
                continue

        return found_entities

    except Exception as e:
        print(f"[ERROR] Failed to fetch or parse {url}: {e}")
        return []

def load_index(index_file="output/index.json"):
    """Load index file containing URLs."""
    try:
        with open(index_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[ERROR] index.json not found.")
        return []

def save_entities(entities, output_file="output/entities.json"):
    """Save extracted entities to JSON file."""
    with open(output_file, "w") as f:
        json.dump(entities, f, indent=2)
    print(f"[✔] Saved {len(entities)} entities to {output_file}")

def main():
    index_data = load_index()
    all_entities = []

    print(f"[→] Crawling {len(index_data)} URLs for structured data...")

    for entry in index_data:
        url = entry.get("url")
        if url:
            entities = extract_json_ld_entities(url)
            all_entities.extend(entities)

    save_entities(all_entities)

if __name__ == "__main__":
    main()
#         save_to_json(entity)