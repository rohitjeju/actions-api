import requests
import json

def consume_api():
    # Define the API endpoint URL
    url = "http://localhost:8000/"
    
    try:
        # Send GET request to the API
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print("Received data from API:")
            print(json.dumps(data, indent=2))
            return data
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None

if __name__ == "__main__":
    consume_api()
