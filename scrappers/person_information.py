import requests
import os
from dotenv import load_dotenv
load_dotenv()

PERSON_API_KEY = os.getenv("FIND_PERSON_API")

def find_person(name, api_key=PERSON_API_KEY, city=None, state_code=None, street_line_1=None, street_line_2=None, postal_code=None, country_code=None):
    """
    Fetch details of a person using the Find Person API and filter results to match first and last names.

    :param api_key: str - Your API key for authentication.
    :param name: str - The name of the person to search for.
    :param city: str (optional) - The city of the person's address.
    :param state_code: str (optional) - The state code of the person's address.
    :param street_line_1: str (optional) - The first line of the street part of the address.
    :param street_line_2: str (optional) - The second line of the street part of the address.
    :param postal_code: str (optional) - The postal code of the address.
    :param country_code: str (optional) - The ISO-3166 alpha-2 country code of the address.

    :return: dict - The filtered JSON response from the API.
    """
    url = "https://api.trestleiq.com/3.1/person"

    params = {"name": name}
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

    headers = {"x-api-key": api_key}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            if 'person' in result and isinstance(result['person'], list):
                name_parts = name.strip().split()
                input_first = (name_parts[0].lower() if name_parts else '')
                input_last = (name_parts[-1].lower() if len(name_parts) > 1 else '')

                filtered_people = []
                for person in result['person']:
                    p_first = (person.get('firstname', '') or '').strip().lower()
                    p_last = (person.get('lastname', '') or '').strip().lower()

                    if p_first == input_first and p_last == input_last:
                        filtered_people.append(person)
                
                result['person'] = filtered_people
                result['count_person'] = len(filtered_people)
            return result
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
