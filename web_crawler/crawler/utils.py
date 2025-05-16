from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json

# Function to clean and standardize URLs
def clean_url(link, base_url):
    # Ensure the link is an absolute URL
    if link.startswith('http'):
        return link
    return urljoin(base_url, link)

# Check if the URL is internal (same domain)
def is_internal_link(link, base_url):
    base_parsed = urlparse(base_url)
    link_parsed = urlparse(link)

    # Check if the base domain matches the link's domain
    return base_parsed.netloc == link_parsed.netloc

# Extract meta tags (like title, description, etc.)
def extract_meta_tags(soup):
    meta_tags = {}
    # Extract meta tags and their content
    for tag in soup.find_all('meta'):
        if 'name' in tag.attrs:
            name = tag.attrs['name'].lower()
            if name in ['robots', 'description', 'keywords']:
                meta_tags[name] = tag.attrs.get('content', '')
    return meta_tags

# Extract schema.org data (JSON-LD and Microdata)
def extract_schema(soup):
    schema_data = []

    # Look for JSON-LD (structured data)
    json_ld = soup.find_all('script', type='application/ld+json')
    for item in json_ld:
        try:
            schema_data.append(json.loads(item.string))
        except json.JSONDecodeError:
            continue

    # You can also extract other formats like Microdata if necessary.
    # This example only supports JSON-LD for simplicity.

    return schema_data
