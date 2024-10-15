import requests
import json
import pandas as pd
import csv

# API endpoint
url = "https://sms.federalseed.gov.pk/api/Seed/GetAllSamplingRequestByProcForPrintery"

# Authorization token
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjpbInByaW50ZXJ5LjFAZmVkZXJhbHNlZWQuZ292LnBrIiwiTWlyemEgU2V3IFRlY2giXSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoicHJpbnRlcnkuMUBmZWRlcmFsc2VlZC5nb3YucGsiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiIwNTFjZjBjMi1jNmU3LTQ2MGItOTkzOC1hYmU4NmZhNzdiMzkiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJwcmludGVyeSIsIi8vUGFyYWRpZ20vY2xhaW1zL2N1bHR1cmVuYW1lIjoiZW4iLCIvL1BhcmFkaWdtL2NsYWltcy90aW1lem9uZWlkIjoiUGFraXN0YW4gU3RhbmRhcmQgVGltZSIsIi8vUGFyYWRpZ20vY2xhaW1zL2ZpbmdlcnByaW50IjoiYXFidU14ejM3TkRtYzZsalNnd2p3Mm1BY3Y0U1JkMERWSnNvSUlWMFZWMUxpeGN1OUNkelg3ZHRLQXd5cHg0c3pqZUZNWXovZ1BDNGVvU1RXMW80VkN2UXczcU8zWjJ3ZGVQcm4vNkJaNG5JdVk0S2lLcTBvTlpFY3E4TVNEcThSVHljZ01jaExhVC9sandpL0loR3liam9aTit5WnI2L2ZYbkNQNnc2WnNjPSIsIi8vUGFyYWRpZ20vY2xhaW1zL3ZlcmlmaWVkIjoiZmFsc2UiLCJzdWIiOiJwcmludGVyeS4xQGZlZGVyYWxzZWVkLmdvdi5wayIsIkF1ZGl0U2Vzc2lvbiI6IjIzMTA4YTAyLTRiODAtNGJmNC1hN2MzLWVhNmMyNzNmN2U5NiIsInVzZXJfdHlwZSI6IlBSSU5URVJZIiwiY29tcGFueV9pZCI6IjEiLCJjb21wYW55X25hbWUiOiJFbXBpcmUgU2VlZDEiLCJ1c2VySWQiOiIwNTFjZjBjMi1jNmU3LTQ2MGItOTkzOC1hYmU4NmZhNzdiMzkiLCJpc1N1cGVyQWRtaW4iOiJGQUxTRSIsIm5iZiI6MTcyMzI4NDY3NywiZXhwIjoxNzIzODkzMDc3LCJpc3MiOiJsb2NhbGhvc3QiLCJhdWQiOiJybXNhcHAifQ.h6F8stEGcB3gKjvsXFEDv2rIYoPasWauluNkSYIzGos"

# Headers
headers = {
    "Authorization": token,
    "Content-Type": "application/json"
}

# Request body with provided parameters
data = {
    "start": 0,
    "limit": 16505,
    "sort": None,
    "order": "desc",
    "companyId": None,
    "currentStatus": None,
    "cropId": None,
    "categoryName": None,
    "varietyId": None
}

# Making the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    response_data = response.json()  # Extracting data in JSON format

    # Assuming the response data contains a key 'data' with the required information
    if 'data' in response_data:
        df = pd.DataFrame(response_data['data'])  # Create DataFrame from the data

      
        df.to_csv('sampling_requests.txt', index=False)
        print("Data saved to sampling_requests.txt")
    else:
        print("No 'data' key found in the response")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)



csv.field_size_limit(1000000000)  # Set a suitable limit depending on your data size

# File paths
input_file = r"sampling_requests.txt"
output_file = r"parsed_data.csv"

try:
    # Step 1: Read the content of the text file
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.read().strip().split("\n")

    # Step 2: Extract the relevant CSV part
    csv_header = lines[0]
    csv_data = lines[1:]

    # Step 3: Parse the CSV content
    reader = csv.DictReader([csv_header] + csv_data)

    parsed_records = []

    # Step 4: Process each row to replace single quotes with double quotes and parse the JSON data
    for row in reader:
        try:
            success = row['success']
            data = row['data'].replace("'", "\"")
            records = json.loads(data)
            if isinstance(records, list):
                parsed_records.extend(records)
            else:
                print(f"Warning: Expected a list of records but got {type(records)}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except KeyError as e:
            print(f"Missing key: {e}")

    # Step 5: Write the parsed data to a new CSV file
    if parsed_records:
        # Extract all unique field names from parsed records
        fieldnames = set()
        for record in parsed_records:
            fieldnames.update(record.keys())

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in parsed_records:
                writer.writerow(record)

        print(f"Data has been successfully written to {output_file}")
    else:
        print("No valid records to write.")

except FileNotFoundError:
    print(f"File not found: {input_file}")

except Exception as e:
    print(f"Error: {str(e)}") 