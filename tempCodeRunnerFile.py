import requests
import json

# API endpoint
url = "https://sms.federalseed.gov.pk/api/Seed/GetAllCompany"

# Authorization token
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjpbInByaW50ZXJ5LjFAZmVkZXJhbHNlZWQuZ292LnBrIiwiTWlyemEgU2V3IFRlY2giXSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoicHJpbnRlcnkuMUBmZWRlcmFsc2VlZC5nb3YucGsiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiIwNTFjZjBjMi1jNmU3LTQ2MGItOTkzOC1hYmU4NmZhNzdiMzkiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJwcmludGVyeSIsIi8vUGFyYWRpZ20vY2xhaW1zL2N1bHR1cmVuYW1lIjoiZW4iLCIvL1BhcmFkaWdtL2NsYWltcy90aW1lem9uZWlkIjoiUGFraXN0YW4gU3RhbmRhcmQgVGltZSIsIi8vUGFyYWRpZ20vY2xhaW1zL2ZpbmdlcnByaW50IjoiYXFidU14ejM3TkRtYzZsalNnd2p3Mm1BY3Y0U1JkMERWSnNvSUlWMFZWMUxpeGN1OUNkelg3ZHRLQXd5cHg0c3pqZUZNWXovZ1BDNGVvU1RXMW80VkN2UXczcU8zWjJ3ZGVQcm4vNkJaNG5JdVk0S2lLcTBvTlpFY3E4TVNEcThSVHljZ01jaExhVC9sandpL0loR3liam9aTit5WnI2L2ZYbkNQNnc2WnNjPSIsIi8vUGFyYWRpZ20vY2xhaW1zL3ZlcmlmaWVkIjoiZmFsc2UiLCJzdWIiOiJwcmludGVyeS4xQGZlZGVyYWxzZWVkLmdvdi5wayIsIkF1ZGl0U2Vzc2lvbiI6IjIzMTA4YTAyLTRiODAtNGJmNC1hN2MzLWVhNmMyNzNmN2U5NiIsInVzZXJfdHlwZSI6IlBSSU5URVJZIiwiY29tcGFueV9pZCI6IjEiLCJjb21wYW55X25hbWUiOiJFbXBpcmUgU2VlZDEiLCJ1c2VySWQiOiIwNTFjZjBjMi1jNmU3LTQ2MGItOTkzOC1hYmU4NmZhNzdiMzkiLCJpc1N1cGVyQWRtaW4iOiJGQUxTRSIsIm5iZiI6MTcyMzI4NDY3NywiZXhwIjoxNzIzODkzMDc3LCJpc3MiOiJsb2NhbGhvc3QiLCJhdWQiOiJybXNhcHAifQ.h6F8stEGcB3gKjvsXFEDv2rIYoPasWauluNkSYIzGos"

# Headers
headers = {
    "Authorization": token,
    "Content-Type": "application/json"
}

# Making the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    response_data = response.json()  # Extracting data in JSON format

    # Save the raw JSON data to a text file
    with open('response_data.txt', 'w') as file:
        json.dump(response_data, file, indent=2)  # Save with indentation for readability

    # Extract company names from the saved data
    companies = response_data.get('data', [])
    company_names = [company['text'].strip() for company in companies if isinstance(company, dict)]

    # Save the company names to a separate text file
    with open('company_names.txt', 'w') as file:
        for name in company_names:
            file.write(name + '\n')

    print("Data saved to 'response_data.txt' and company names saved to 'company_names.txt'.")
else:
    print(f"Request failed with status code {response.status_code}")
