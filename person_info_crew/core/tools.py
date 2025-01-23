# person_info_crew/core/tools.py
from crewai import Tool
from config.settings import config
from core.memory import memory
import requests

def find_person(
    name: str, 
    city: str = None, 
    state_code: str = None,
    street_line_1: str = None,
    street_line_2: str = None,
    postal_code: str = None,
    country_code: str = None
) -> dict:
    """Fetch details of a person using the Find Person API."""
    @memory.cached
    def _search(**params):
        url = "https://api.trestleiq.com/3.1/person"
        headers = {"x-api-key": config.person_api_key}
        
        # Structure address parameters
        address_params = {}
        if city: address_params["city"] = city
        if state_code: address_params["state_code"] = state_code
        if street_line_1: address_params["street_line_1"] = street_line_1
        if street_line_2: address_params["street_line_2"] = street_line_2
        if postal_code: address_params["postal_code"] = postal_code
        if country_code: address_params["country_code"] = country_code
        
        params = {"name": name}
        if address_params:
            params["address"] = address_params

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            return {
                "error": f"API error {response.status_code}",
                "details": response.text
            }
        except requests.RequestException as e:
            return {"error": str(e)}
    
    return _search(
        name=name,
        city=city,
        state_code=state_code,
        street_line_1=street_line_1,
        street_line_2=street_line_2,
        postal_code=postal_code,
        country_code=country_code
    )

def google_search(query: str) -> list:
    """Search Google using Custom Search JSON API."""
    @memory.cached
    def _search(query):
        url = f'https://www.googleapis.com/customsearch/v1'
        params = {
            'key': config.google_api_key,
            'cx': config.google_cse_id,
            'q': query,
            'num': 3
        }
        
        try:
            response = requests.get(url, params=params)
            results = response.json()
            items = results.get('items', [])
            return [
                {"url": item.get('link'), "snippet": item.get('snippet')}
                for item in items
            ]
        except Exception as e:
            return [{"error": str(e)}]
    
    return _search(query)

def query_parser(query: str) -> dict:
    """Parse natural language queries to structured parameters."""
    from crewai import Agent
    parser = Agent(
        role="Query Analyzer",
        goal="Extract search parameters from natural language",
        backstory="Specializes in understanding human language queries",
        verbose=True
    )
    
    return parser.parse_input(
        f"""Analyze this query: {query}
        Extract and return JSON with:
        - name
        - postal_code
        - city
        - state_code  
        - street_line_1
        - street_line_2
        - country_code
        - requested_fields"""
    )

# Tool definitions
person_search_tools = [
    Tool(
        name="Person Search API",
        func=find_person,
        description="""
        Primary source for verified personal information. Use when you have:
        - Full name plus at least one address component (postal code, city, etc)
        - Requires at least a name and partial address info
        Returns: Detailed contact info including email, phone, addresses
        """
    ),
    Tool(
        name="Google Search",
        func=google_search,
        description="""
        Secondary source for public information. Use when:
        - Primary API fails or returns incomplete data
        - No address information available
        - Need supplemental web results
        Returns: List of relevant URLs with snippets
        """
    ),
    Tool(
        name="Query Analyzer",
        func=query_parser,
        description="Extracts structured search parameters from natural language queries"
    )
]