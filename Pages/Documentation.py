import streamlit as st

def documentation_page():
    st.title("Documentation: Person Data Finder")

    st.markdown("""
    ## Overview
    Welcome to the **Person Data Finder**! This tool allows you to fetch contact details and related information about individuals by simply entering a natural language query. The interface is designed to be straightforward and efficient, offering both on-screen results and an option to download the data in PDF format.

    ## How It Works
    1. **Input a Query:** Enter a query containing the person's name and other address details. Including a postal code is highly recommended for better accuracy.
       - Example query: *"Find contact info for John Doe in New York 10001"*
    2. **Process the Query:** Click the "Process Query" button to fetch the information.
    3. **View the Results:** The contact details will be displayed on the page, including:
        - Email addresses
        - Phone numbers
        - Addresses
        - Related people (if available)
    4. **Download as PDF:** Use the "Download Response as PDF" button to save the results for future use.

    ## Why Single Query Format?
    Instead of implementing a continuous chat feature, we opted for a simple query-response format. This approach is:
    - **Cost-Efficient:** Reduces token consumption in the OpenAI API, saving costs.
    - **Straightforward:** Simplifies the user experience by avoiding unnecessary complexity.

    ## Handling Missing Data
    In some cases, we may not have complete contact details for a query. For such queries, the tool might only provide Google search results, social media links, or other publicly available information.

    ## Key Features
    - **Natural Language Input:** No need for complex syntax or keywords.
    - **Accurate Results:** Leveraging postal codes and specific details improves the accuracy of the response.
    - **PDF Export:** Easily save the results for later use.
    
    ## Example Use Cases
    - Finding contact details for potential clients.
    - Gathering information about individuals for research or verification purposes.
    - Locating contact information for professional networking.

    ## Limitations
    - Data availability depends on the completeness of publicly accessible information.
    - For some individuals, only partial or no details may be retrievable.

    ## Contact Us
    If you have any questions, feedback, or need assistance, please feel free to reach out to our support team.

    Thank you for using the Person Data Finder!
    """)

if __name__ == "__main__":
    documentation_page()
