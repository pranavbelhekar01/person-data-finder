from openai import OpenAI
from dotenv import load_dotenv
import os
import json
## other files
from scrappers.person_information import find_person
from scrappers.scrapper1 import google_search
from scrappers.templates import agent_prompt, extraction_prompt
from dotenv import load_dotenv
load_dotenv()

PERSON_API_KEY = os.getenv("FIND_PERSON_API")

API_KEY = os.getenv("SECRET_OPENAI_API")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=API_KEY,  
)
mini_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=API_KEY,  

)

def get_info(name, information):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                agent_prompt,
            ),
            # ("human", "{data}"),
        ]
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "name": name,
            "data": information,
            
        }
    )

    return response.content

def extract_parameters(query):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                extraction_prompt,
            ),
            
        ]
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "query": query,
            
        }
    )

    return response.content


def get_data(query):
    name = "" 
    api_key = PERSON_API_KEY
    city=None
    state_code=None
    street_line_1=None 
    street_line_2=None 
    postal_code=None
    country_code=None
    other_info=None
    parameters = extract_parameters(query)
    try:
        parameters = json.loads(parameters)
        if "name" in parameters:
            name = parameters["name"]
        if "api_key" in parameters:
            api_key = parameters["api_key"]
        if "city" in parameters:
            city = parameters["city"]
        if "state_code" in parameters:
            state_code = parameters["state_code"]
        if "street_line_1" in parameters:
            street_line_1 = parameters["street_line_1"]
        if "street_line_2" in parameters:
            street_line_2 = parameters["street_line_2"]
        if "postal_code" in parameters:
            postal_code = parameters["postal_code"]
        if "country_code" in parameters:
            country_code = parameters["country_code"]
        if "other_info" in parameters:
            other_info = parameters["other_info"]
    except:
        return "Please provide a valid query. Name with some other information such as postal code or city name or address is required."
    person_information = find_person(name, api_key, city, state_code, street_line_1, street_line_2, postal_code, country_code)
    if other_info:
        google_query = f'"{name}" {other_info}'
        google_information = google_search(google_query)
    else:
        google_query = f'"{name}"'
        google_information = google_search(google_query)

    information = {
        "person_information": person_information,
        "google_information": google_information
    }
    information_string = json.dumps(information)
    llm_response = get_info(name, information_string)
    
    return llm_response


# if __name__ == "__main__":
#     name = ""
#     city = ""
#     state_code = ""
#     street_line_1 = ""
#     street_line_2 = ""
#     postal_code = ""
#     flag = True

#     pass