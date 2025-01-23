from crewai import Agent
from person_info_crew.config.settings import config
from person_info_crew.core.tools import person_search_tools

class PersonResearchAgent:
    @classmethod
    def create(cls):
        return Agent(
            role="Personal Information Specialist",
            goal="Retrieve and validate personal information from multiple sources",
            backstory="Expert in cross-referencing API data with public records",
            tools=person_search_tools,
            verbose=True,
            memory=True,
            allow_delegation=False,
            max_iter=5,
            llm=config.llm_config  # Make sure config is properly imported
        )