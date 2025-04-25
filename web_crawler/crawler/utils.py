from urllib.parse import urljoin, urlparse

# Function to clean and standardize URLs
def clean_url(link, base_url):
    if link.startswith('http'):
        return link
    return urljoin(base_url, link)
