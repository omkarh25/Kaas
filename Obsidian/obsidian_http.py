import requests

# Define the base URL and endpoint
base_url = "http://127.0.0.1:27123/"  # Replace PORT with the actual port number
endpoint = "/active/"

YOUR_API_KEY ="229a358b9a2eb7595941240561678c38234812b5e20cd7d193c0a770616583fb"

# Define the headers
headers = {
    "Accept": "application/vnd.olrapi.note+json",  # Specify the desired response format
    "Authorization": f"Bearer {YOUR_API_KEY}"  # Use the api_key variable
}

# Make the GET request
response = requests.get(base_url + endpoint, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print("Response Content:")
    print(response.json())
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    print("Response Content:")
    print(response.text)
