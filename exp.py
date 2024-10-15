import requests

def check_api_connection_with_token(url, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Connected to {url} successfully. Status code: {response.status_code}")
        return True
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return False

# Example usage
protected_api_url = "https://sms.federalseed.gov.pk/api/auth/Login"  # Replace with an endpoint that requires token
api_token = "CfDJ8Hxs1UbYByRLh2MpGjgsB6sC2NQU8GxHlQ94oBvrrfuDUgkfO1ty6SzbWD6PbrWp9HOc3_IbeuKLSqkEAZ8Rs54voI9RMSllY8GAsQIxoY8DzeWys0oBp8rSuOIvsH4PNjNNxZZOSzuros_PK6H4BStXTm8dLfPLdPExec4Cn5e_XYJqENMbPSul2N6yUtCJuw; perf_dv6Tr4n=1"  # Replace with your actual token
is_connected = check_api_connection_with_token(protected_api_url, api_token)
