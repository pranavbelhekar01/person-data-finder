from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from dotenv import load_dotenv
load_dotenv()
import os

os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CX")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")



search = GoogleSearchAPIWrapper()

tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
)

result = tool.run('"Galen Massey"')
print(result)