import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Retrieve the API key from environment variable
API_KEY = os.getenv("PERPLEXITY_API_KEY")


def query_llm(user_query):
    
    # Retrieve the API key from environment variable
    prompt = """
    You are helpful agent that scrapes data from the internet. You will be provided with the person name and may be other little specific details.
    Your task is to provide the contact details that are available on the internet. Check the USA publically available databases, pdf, documents, social media.
    Provide only 3 things of related person- email addresses, phone/contact number, address
    Json response is preferable. Do not provide unnecessary extra information.

    """
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {   
            "role": "user",
            "content": user_query,
        },
    ]

    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,
    )
    print(response)

   

    return response
  

# Example usage
if __name__ == "__main__":
    user_input = input("Enter your query: ")
    response = query_llm(user_input)
    print("Response from LLM:", response)
