import os
from crewai import LLM
import litellm

class Settings:
    @property
    def person_api_key(self) -> str:
        """API key for the Person Search service"""
        return os.getenv("FIND_PERSON_API")
    
    @property
    def google_api_key(self) -> str:
        """Google Custom Search JSON API key"""
        return os.getenv("GOOGLE_API_KEY")
    
    @property
    def google_cse_id(self) -> str:
        """Google Custom Search Engine ID"""
        return os.getenv("GOOGLE_CX")
    
    @property
    def llm_config(self):
        litellm.set_verbose = True
        return LLM(
            model="gpt-4o-mini",
            api_key=os.getenv("SECRET_OPENAI_API"),
            temperature=0,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            timeout=30,
            max_retries=2,
            
        )
config = Settings()