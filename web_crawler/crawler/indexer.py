import json
import os

# Output file for storing indexed data
output_dir = os.path.join(os.path.dirname(__file__), '../output')
output_file = os.path.join(output_dir, 'entities.json')

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize the JSON data structure
if not os.path.exists(output_file):
    with open(output_file, 'w') as f:
        json.dump([], f)

# Function to save crawled entity data to the JSON file
def save_to_json(entity):
    # Read current data from file
    with open(output_file, 'r') as f:
        data = json.load(f)
    
    # Append new entity to the list
    data.append(entity)

    # Save updated data back to the file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
