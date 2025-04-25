import json
import os

# Output file for storing indexed data
output_file = os.path.join(os.path.dirname(__file__), '../output/index.json')

# Initialize the JSON data structure
if not os.path.exists(output_file):
    with open(output_file, 'w') as f:
        json.dump([], f)

# Function to save crawled URLs to the JSON file
def save_to_json(url):
    # Read current data from file
    with open(output_file, 'r') as f:
        data = json.load(f)
    
    # Append new URL to the list
    data.append({"url": url})

    # Save updated data back to the file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)