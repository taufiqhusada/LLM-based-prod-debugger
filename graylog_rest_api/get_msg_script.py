import requests
from requests.auth import HTTPBasicAuth
import json

# Graylog API endpoint for searching logs
graylog_api_url = "http://localhost:9000/api/views/search/messages"

# Basic Auth credentials
username = "admin"
password = "yourpassword"

# Set headers including Basic Auth credentials
headers = {
    'Accept': 'text/csv',
    "Content-Type": "application/json",
    # 'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'X-Requested-By': 'Graylog API Browser',
}

# Define the search parameters
search_params = {
    "streams": [
        "000000000000000000000001"
    ],
    
    "timerange": {
        "type": "relative",
        "range": 9000000
    },

    "fields_in_order": [
       "timestamp","source", "message", "movieDetails", "searchTerm", "error", "level"
    ]
}

# Make the API call with Basic Authentication
response = requests.post(graylog_api_url, headers=headers, auth=HTTPBasicAuth(username, password), data=json.dumps(search_params))


# Check if the request was successful
if response.status_code == 200:
    # Print the response data
    print(response.text)
else:
    print(f"Error: {response.status_code} - {response.text}")
