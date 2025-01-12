import requests
import json

def search_profiles(api_token, search_params):
    """
    Search for profiles using the ContactOut People Search API.

    :param api_token: Your API token for ContactOut.
    :param search_params: A dictionary containing the search parameters.
    :return: The JSON response from the API or an error message.
    """
    url = "https://api.contactout.com/v1/people/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "basic",
        "token": api_token
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(search_params))
        
        # Check for HTTP request errors
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}: {response.text}"}

        # Return the JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Example Usage
if __name__ == "__main__":
    api_token = "LsFIEKnY5u5TbtvGHLEQ9xSQ"
    search_params = {
        "page": 1,
        "name": "Galen Massey",
        "reveal_info": True
    }

    result = search_profiles(api_token, search_params)
    
    # Print formatted JSON response
    print(json.dumps(result, indent=4))