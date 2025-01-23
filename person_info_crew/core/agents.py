from crewai import Agent
from config.settings import config
from core.tools import person_search_tools

class PersonResearchAgent:
    @classmethod
    def create(cls):
        return Agent(
            role="Senior Personal Information Researcher",
            goal="""Retrieve accurate personal information while optimizing 
                   API usage and maintaining data privacy""",
            backstory="""A seasoned investigator with expertise in cross-referencing 
                       multiple data sources and validating information reliability.""",
            tools=person_search_tools,
            verbose=True,
            memory=True,
            allow_delegation=False,
            max_iter=5,
            llm=config.llm_config
        )