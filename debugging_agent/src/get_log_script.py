import requests
from requests.auth import HTTPBasicAuth
import json
import csv
from io import StringIO

def get_recent_logs():
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
            "range": 900
        },

        "fields_in_order": [
            "gl2_message_id", "timestamp","source", "message", "movieDetails", "searchTerm", "error", "level"
        ]
    }

    # Make the API call with Basic Authentication
    response = requests.post(graylog_api_url, headers=headers, auth=HTTPBasicAuth(username, password), data=json.dumps(search_params))


    # Check if the request was successful
    if response.status_code == 200:
        # Print the response data
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)
        json_response = json.dumps(list(reader))
        
        with open('../temp/log.json', 'w') as json_file:
            json_file.write('{"data": ' + json_response + '}')

        return "JSON response saved to 'log.json' file."
    else:
        return "Error: {response.status_code} - {response.text}"
