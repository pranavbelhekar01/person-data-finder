from crewai import Crew, Process
from person_info_crew.core.agents import PersonResearchAgent
from person_info_crew.core.tasks import PersonInfoTasks
from person_info_crew.utils.formatters import format_person_info
from dotenv import load_dotenv

load_dotenv()

class PersonInfoCrew:
    def __init__(self):
        self.researcher = PersonResearchAgent.create()
        
    def assemble_crew(self):
        return Crew(
            agents=[self.researcher],
            tasks=[
                PersonInfoTasks.information_retrieval(self.researcher),
                PersonInfoTasks.format_response(self.researcher)
            ],
            process=Process.hierarchical,
            verbose=2,
            memory=True
        )

    def run(self, query):
        crew = self.assemble_crew()
        result = crew.kickoff(inputs={'input': query})
        return format_person_info(result)

if __name__ == "__main__":
    crew = PersonInfoCrew()
    
    # Example conversation flow
    queries = [
        "Find contact info for Galen massey in 90210",
        "What's his email address?",
        "Any phone numbers associated with him?"
    ]
    
    for query in queries:
        print(f"User Query: {query}")
        response = crew.run(query)
        print(f"Agent Response:\n{response}\n{'='*50}")