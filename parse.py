import csv
import json

# Define file paths
input_file = 'response_data.txt'
output_file = 'response_data.csv'

# Read the JSON data from the text file
with open(input_file, 'r') as file:
    json_data = file.read()

# Parse JSON data
data = json.loads(json_data)

# Extract the relevant part of the data
items = data['data']['data']

# Write to CSV
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['id', 'text'])
    # Write data
    for item in items:
        writer.writerow([item['id'], item['text']])

print(f'CSV file "{output_file}" has been created successfully.')
