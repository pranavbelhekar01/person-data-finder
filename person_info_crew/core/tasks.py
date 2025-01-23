from crewai import Task

class PersonInfoTasks:
    @classmethod
    def information_retrieval(cls, agent):
        return Task(
            description="""Extract personal information from user query:
                        {input}
                        
                        Process:
                        1. Parse query parameters
                        2. Check memory cache
                        3. Use Person API first
                        4. Fallback to Google Search if needed
                        5. Validate data consistency""",
            expected_output="Structured JSON with verified personal information",
            agent=agent,
            output_file="person_data.json"
        )

    @classmethod
    def format_response(cls, agent):
        return Task(
            description="""Convert raw data to user-friendly format.
                        Include default fields (email, address, phone) if none specified.
                        Handle missing data gracefully.""",
            expected_output="Well-formatted response in natural language",
            agent=agent,
            output_file="formatted_response.md",
            context=[]
        )