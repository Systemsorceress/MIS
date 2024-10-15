import requests
import json
import pandas as pd
import csv


# Function to read the last row index from a CSV file
def get_last_row_value(file_path):
    try:
        df = pd.read_csv(file_path)
        if not df.empty:
            return df.iloc[-1].name + 1  # Assuming index is zero-based
        else:
            return 0
    except FileNotFoundError:
        return 0  # Return 0 if file not found


# Paths to the CSV files
parsed_data1_file = r"C:\Users\Malaika\OneDrive\Desktop\Fscrd\parsed_data1.csv"
parsed_data_file = r"C:\Users\Malaika\OneDrive\Desktop\Fscrd\parsed_data.csv"
parsed_data2_file = r"C:\Users\Malaika\OneDrive\Desktop\Fscrd\parsed_data2.csv"


# Read the last row values
max_value = get_last_row_value(parsed_data1_file)
min_value = get_last_row_value(parsed_data_file)


# Calculate the limit
limit = max_value - min_value


# API endpoint
url = "https://sms.federalseed.gov.pk/api/Seed/GetAllSamplingRequestByProcForPrintery"


# Authorization token
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjpbInByaW50ZXJ5LjFAZmVkZXJhbHNlZWQuZ292LnBrIiwiTWlyemEgU2V3IFRlY2giXSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoicHJpbnRlcnkuMUBmZWRlcmFsc2VlZC5nb3YucGsiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiIwNTFjZjBjMi1jNmU3LTQ2MGItOTkzOC1hYmU4NmZhNzdiMzkiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJwcmludGVyeSIsIi8vUGFyYWRpZ20vY2xhaW1zL2N1bHR1cmVuYW1lIjoiZW4iLCIvL1BhcmFkaWdtL2NsYWltcy90aW1lem9uZWlkIjoiUGFraXN0YW4gU3RhbmRhcmQgVGltZSIsIi8vUGFyYWRpZ20vY2xhaW1zL2ZpbmdlcnByaW50IjoiYXFidU14ejM3TkRtYzZsalNnd2p3Mm1BY3Y0U1JkMERWSnNvSUlWMFZWMUxpeGN1OUNkelg3ZHRLQXd5cHg0c3pqZUZNWXovZ1BDNGVvU1RXMW80VkN2UXczcU8zWjJ3ZGVQcm4vNkJaNG5JdVk0S2lLcTBvTlpFY3E4TVNEcThSVHljZ01jaExhVC9sandpL0loR3liam9aTit5WnI2L2ZYbkNQNnc2WnNjPSIsIi8vUGFyYWRpZ20vY2xhaW1zL3ZlcmlmaWVkIjoiZmFsc2UiLCJzdWIiOiJwcmludGVyeS4xQGZlZGVyYWxzZWVkLmdvdi5wayIsIkF1ZGl0U2Vzc2lvbiI6IjIzMTA4YTAyLTRiODAtNGJmNC1hN2MzLWVhNmMyNzNmN2U5NiIsInVzZXJfdHlwZSI6IlBSSU5URVJZIiwiY29tcGFueV9pZCI6IjEiLCJjb21wYW55X25hbWUiOiJFbXBpcmUgU2VlZDEiLCJ1c2VySWQiOiIwNTFjZjBjMi1jNmU3LTQ2MGItOTkzOC1hYmU4NmZhNzdiMzkiLCJpc1N1cGVyQWRtaW4iOiJGQUxTRSIsIm5iZiI6MTcyMzI4NDY3NywiZXhwIjoxNzIzODkzMDc3LCJpc3MiOiJsb2NhbGhvc3QiLCJhdWQiOiJybXNhcHAifQ.h6F8stEGcB3gKjvsXFEDv2rIYoPasWauluNkSYIzGos"
# Headers
headers = {
    "Authorization": token,
    "Content-Type": "application/json"
}


# Request body with updated parameters (changing order to ascending)
data = {
    "start": 1,
    "limit": limit,
    "sort": None,
    "order": "asc",  # Change order from 'desc' to 'asc'
    "companyId": None,
    "currentStatus": None,
    "cropId": None,
    "categoryName": None,
    "varietyId": None
}


# Making the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))
csv.field_size_limit(100000000)


# Check if the request was successful
if response.status_code == 200:
    response_data = response.json()  # Extracting data in JSON format


    # Assuming the response data contains a key 'data' with the required information
    if 'data' in response_data:
        df = pd.DataFrame(response_data['data'])  # Create DataFrame from the data


        # Save the new data to a temporary file
        temp_file = r"sampling_requests2.txt"
        df.to_csv(temp_file, index=False)
        print("Data saved to sampling_requests2.txt")


        # Read and parse the new data from the text file
        try:
            with open(temp_file, "r", encoding="utf-8") as file:
                lines = file.read().strip().split("\n")


            csv_header = lines[0]
            csv_data = lines[1:]


            reader = csv.DictReader([csv_header] + csv_data)


            parsed_records = []


            for row in reader:
                try:
                    # Ensure the data field exists and is properly formatted
                    if 'data' in row:
                        data = row['data'].replace("'", "\"")
                        records = json.loads(data)
                        if isinstance(records, list):
                            parsed_records.extend(records)
                        else:
                            print(f"Warning: Expected a list of records but got {type(records)}")
                    else:
                        print(f"Warning: 'data' field is missing in row: {row}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                except KeyError as e:
                    print(f"Missing key: {e}")


            if parsed_records:
                # Extract all unique field names from parsed records
                fieldnames = set()
                for record in parsed_records:
                    fieldnames.update(record.keys())


                # Ensure fieldnames are consistent with existing data
                try:
                    with open(parsed_data_file, "r", newline="", encoding="utf-8") as csvfile:
                        reader = csv.DictReader(csvfile)
                        existing_data = list(reader)
                        existing_fieldnames = reader.fieldnames if reader.fieldnames else []
                except FileNotFoundError:
                    existing_data = []
                    existing_fieldnames = []


                # Combine new fieldnames with existing ones
                all_fieldnames = list(set(existing_fieldnames).union(fieldnames))


                with open(parsed_data_file, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames)
                    writer.writeheader()
                   
                    # Write new data first
                    for record in parsed_records:
                        writer.writerow(record)
                   
                    # Write existing data after the new data
                    for row in existing_data:
                        writer.writerow(row)


                print(f"Data has been successfully written to {parsed_data2_file}")
            else:
                print("No valid records to write.")
        except FileNotFoundError:
            print(f"File not found: {temp_file}")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("No 'data' key found in the response")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)