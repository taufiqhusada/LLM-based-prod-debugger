import requests
from requests.auth import HTTPBasicAuth

# Graylog API endpoint for searching logs
graylog_api_url = "http://localhost:9000/api/cluster"

# Basic Auth credentials
username = "admin"
password = "yourpassword"

# Set headers including Basic Auth credentials
headers = {
    "Content-Type": "application/json",
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'X-Requested-By': 'Graylog API Browser',
}

# Make the API call with Basic Authentication
response = requests.get(graylog_api_url, headers=headers, auth=HTTPBasicAuth(username, password))

# Check if the request was successful
if response.status_code == 200:
    # Print the response data
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")