# person_info_crew/core/tools.py
from crewai.tools import BaseTool
from crewai import Agent
from typing import Optional, Dict, Any, List, Type
from pydantic import Field
from person_info_crew.config.settings import config
from person_info_crew.core.memory import memory
import requests
from pydantic import BaseModel, Field


class PersonSearchSchema(BaseModel):
    """Schema for person search parameters"""
    name: str = Field(..., description="Full name of the person to search")
    postal_code: Optional[str] = Field(
        None, 
        description="Postal code of the address (recommended)"
    )
    city: Optional[str] = Field(
        None, 
        description="City of the address (optional)"
    )
    state_code: Optional[str] = Field(
        None, 
        description="State code (2-letter abbreviation, optional)"
    )
    street_line_1: Optional[str] = Field(
        None, 
        description="First street address line (optional)"
    )
    street_line_2: Optional[str] = Field(
        None, 
        description="Second street address line (optional)"
    )
    country_code: Optional[str] = Field(
        None, 
        description="2-letter country code (optional)"
    )

class PersonSearchTool(BaseTool):
    name: str = "Person Search API"
    description: str = """Primary source for verified personal information. 
        Requires at least name and one address component (postal code recommended).
        Returns: Email, phone, addresses"""
    args_schema: Type[BaseModel] = PersonSearchSchema

    def _run(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with flexible parameters"""
        return self.find_person(**kwargs)

    def find_person(
        self,
        name: str,
        postal_code: Optional[str] = None,
        city: Optional[str] = None,
        state_code: Optional[str] = None,
        street_line_1: Optional[str] = None,
        street_line_2: Optional[str] = None,
        country_code: Optional[str] = None
    ) -> dict:
        """Actual API implementation with caching"""
        @memory.cached
        def _search(**params):
            url = "https://api.trestleiq.com/3.1/person"
            headers = {"x-api-key": config.person_api_key}
            
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
                return {"error": f"API error {response.status_code}"}
            except requests.RequestException as e:
                return {"error": str(e)}
        
        return _search(
            name=name,
            postal_code=postal_code,
            city=city,
            state_code=state_code,
            street_line_1=street_line_1,
            street_line_2=street_line_2,
            country_code=country_code
        )
class GoogleSearchTool(BaseTool):
    name: str = Field(
        default="Google Search",
        description="Secondary public information source"
    )
    description: str = Field(
        default=(
            "Use when primary API fails or needs supplemental data. "
            "No address required. Returns: URLs with snippets"
        ),
        description="Tool functionality description"
    )

    def _run(self, query: str) -> List[Dict]:
        @memory.cached
        def _search(query):
            url = 'https://www.googleapis.com/customsearch/v1'

            # url = 'https://randomuser.me/api/'
            params = {
                'key': config.google_api_key,
                'cx': config.google_cse_id,
                'q': query,
                'num': 3
            }
            
            try:
                response = requests.get(url, params=params)
                results = response.json()
                return [
                    {"url": item.get('link'), "snippet": item.get('snippet')}
                    for item in results.get('items', [])
                ]
            except Exception as e:
                print('exception returned')
                return [{"error": str(e)}]
        
        return _search(query)

class QueryParserTool(BaseTool):
    name: str = Field(
        default="Query Analyzer",
        description="Natural language query parser"
    )
    description: str = Field(
        default="Extracts structured parameters from natural language queries",
        description="Tool functionality description"
    )

    def _run(self, query: str) -> Dict[str, str]:
        parser = Agent(
            role="Query Analyzer",
            goal="Convert natural language to structured parameters",
            backstory="Specializes in understanding human language queries",
            verbose=True,
            allow_delegation=False
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

# Tool list initialization
person_search_tools = [
    PersonSearchTool(),
    GoogleSearchTool(),
    QueryParserTool()
]