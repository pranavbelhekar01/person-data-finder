import os

class Settings:
    @property
    def person_api_key(self):
        return os.getenv("FIND_PERSON_API")
    
    @property
    def google_api_key(self):
        return os.getenv("GOOGLE_API_KEY")
    
    @property
    def google_cse_id(self):
        return os.getenv("GOOGLE_CX")
    
    @property
    def llm_config(self):
        return {
            "model": os.getenv("LLM_MODEL", "gpt-4o"),
            "temperature": float(os.getenv("LLM_TEMPERATURE", 0)),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", 0)) or None,
            "timeout": int(os.getenv("LLM_TIMEOUT", 30)),
            "max_retries": int(os.getenv("LLM_MAX_RETRIES", 2)),
            "api_key": os.getenv("SECRET_OPENAI_API", ""),
            "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        }

config = Settings()