import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Retrieve the API key from environment variable
API_KEY = os.getenv("PERPLEXITY_API_KEY")

url = "https://api.perplexity.ai/chat/completions"

prompt = """
You are helpful agent that scrapes data from the internet. You will be provided with the person name and may be other little specific details.
Your task is to provide the contact details that are available on the internet. Check the USA publically available databases, pdf, documents, social media.
Provide only 3 things of related person- email addresses, phone/contact number, address
Json response is preferable. Do not provide unnecessary extra information.
"""

payload = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": "Galen Massey"
        }
    ],
 
    "temperature": 0.2,
    "top_p": 0.9,
    "search_domain_filter": ["linkedin.com", "google.com", "contactout.com", "radris.com", "fullcontant.com", "whitepages.com", "zillow.com", "facebook.com", "wikipedia.org", "data.gov", "guides.library.unt.edu/datasets/public-data-sources", "www.ncdc.noaa.gov", "fivethirtyeight.com", "instagram.com", "census.gov", ],
    "return_images": True,
    "return_related_questions": False,
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1
}
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)