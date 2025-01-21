import requests
from dotenv import load_dotenv
load_dotenv()
import os

API = os.getenv("GOOGLE_API_KEY")
CX_ID = os.getenv("GOOGLE_CX")

def google_search(query):
    api_key = API  
    cx = CX_ID     

    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q="{query}"'
    response = requests.get(url)
    results = response.json()
    items = results.get('items', [])

    urls = []
    snippets = []

    for item in items:
        link = item.get('link', 'N/A')
        snippet = item.get('snippet', 'N/A')
        urls.append(link)
        snippets.append(snippet)

    # Create a JSON object zipping URLs with snippets
    zipped_results = [
        {"url": url, "snippet": snippet} for url, snippet in zip(urls, snippets)
    ]

    return zipped_results


if __name__ == "__main__":
    result = google_search("Galen Massey")
    print(result)
    print("Length of result:: ", len(result))
    print(f'Type of result:: {type(result)}')
    