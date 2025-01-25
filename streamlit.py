import streamlit as st
from suppplimentary import get_data

def main():
    st.title("Natural Language Query Interface")

    # Input field for natural language query
    query = st.text_input("Enter your query (required)", 
                         placeholder="e.g., 'Find contact info for John Doe in New York'",
                         key="query_input")

    # Submit button
    if st.button("Process Query"):
        # Validate required field
        if not query.strip():
            st.error("Please enter a query before submitting.")
        else:
            # Call the function with the provided query
            with st.spinner('Processing your query...'):
                try:
                    response = get_data(query=query.strip())
                    st.markdown(f"### Query Results:\n{response}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()