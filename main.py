from openai import OpenAI
from dotenv import load_dotenv
import os
import json
## other files
from scrappers.person_information import find_person
from scrappers.scrapper1 import google_search
from scrappers.templates import agent_prompt
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

def get_info(information):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                agent_prompt,
            ),
            ("human", "{contact_data}"),
        ]
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "contact_data": information,
        }
    )
    return response.content



def get_data(name, api_key = PERSON_API_KEY, city=None, state_code=None, street_line_1=None, street_line_2=None, postal_code=None, country_code=None):
    person_information = find_person(name, api_key, city, state_code, street_line_1, street_line_2, postal_code, country_code)
    google_information = google_search(name)
    information = {
        "person_information": person_information,
        "google_information": google_information
    }
    information_string = json.dumps(information)
    llm_response = get_info(information_string)
    
    return llm_response


if __name__ == "__main__":
    name = ""
    city = ""
    state_code = ""
    street_line_1 = ""
    street_line_2 = ""
    postal_code = ""
    flag = True

    pass