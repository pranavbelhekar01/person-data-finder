from openai import OpenAI
from dotenv import load_dotenv
import os
from scrappers.contactout import search_profiles
load_dotenv()

API_KEY = os.getenv("SECRET_OPENAI_API")
# client = OpenAI(api_key=API_KEY)

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

def get_info(query):

    information = search_profiles(query)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that translates {input_language} to {output_language}.",
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "input_language": "English",
            "output_language": "German",
            "input": information,
        }
    )


if __name__ == "__main__":
    pass