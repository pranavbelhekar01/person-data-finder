import requests
import os
from dotenv import load_dotenv
load_dotenv()

PERSON_API_KEY = os.getenv("FIND_PERSON_API")

def find_person(name, api_key = PERSON_API_KEY, city=None, state_code=None, street_line_1=None, street_line_2=None, postal_code=None, country_code=None):
    """
    Fetch details of a person using the Find Person API.

    :param api_key: str - Your API key for authentication.
    :param name: str - The name of the person to search for.
    :param city: str (optional) - The city of the person's address.
    :param state_code: str (optional) - The state code of the person's address.
    :param street_line_1: str (optional) - The first line of the street part of the address.
    :param street_line_2: str (optional) - The second line of the street part of the address.
    :param postal_code: str (optional) - The postal code of the address.
    :param country_code: str (optional) - The ISO-3166 alpha-2 country code of the address.

    :return: dict - The JSON response from the API.
    """
    url = "https://api.trestleiq.com/3.1/person"

    # Construct query parameters
    params = {
        "name": name
    }

    if city:
        params["address.city"] = city
    if state_code:
        params["address.state_code"] = state_code
    if street_line_1:
        params["address.street_line_1"] = street_line_1
    if street_line_2:
        params["address.street_line_2"] = street_line_2
    if postal_code:
        params["address.postal_code"] = postal_code
    if country_code:
        params["address.country_code"] = country_code

    # Set headers
    headers = {
        "x-api-key": api_key
    }

    try:
        # Make the API request
        response = requests.get(url, headers=headers, params=params)

        # Check for successful response
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API returned status code {response.status_code}",
                "details": response.text
            }

    except requests.RequestException as e:
        return {
            "error": "An error occurred while making the API request.",
            "details": str(e)
        }

# Example usage
if __name__ == "__main__":
    API_KEY = PERSON_API_KEY
    NAME = "Galen Massey"
    result = find_person(api_key = API_KEY, name = NAME, postal_code="28206")
    print(result)
