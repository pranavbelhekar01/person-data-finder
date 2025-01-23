import streamlit as st
from suppplimentary import get_data

# def get_data(name, postal_code, city=None, state_code=None, street_line_1=None, street_line_2=None, other_info=None):
#     """
#     Mock function to handle submitted data.
#     Replace with your desired implementation.
#     """
#     response = f"Received data:\nName: {name}\nPostal Code: {postal_code}\nCity: {city or 'N/A'}\nState Code: {state_code or 'N/A'}\nStreet Line 1: {street_line_1 or 'N/A'}\nStreet Line 2: {street_line_2 or 'N/A'}"
#     return response

# Streamlit form
def main():
    st.title("Information Form")

    # Input fields
    name = st.text_input("Name (required)", "")
    postal_code = st.text_input("Postal Code (required)", "")
    city = st.text_input("City (optional)", "")
    state_code = st.text_input("State Code (optional)", "")
    street_line_1 = st.text_input("Street Line 1 (optional)", "")
    street_line_2 = st.text_input("Street Line 2 (optional)", "")
    other_info = st.text_input("Other Information (e.g. profession, company, etc.) (optional)", "")

    # Submit button
    if st.button("Submit"):
        # Validate required fields
        if not name.strip():
            st.error("Name is required.")
        elif not postal_code.strip():
            st.error("Postal Code is required.")
        else:
            # Call the function with provided data
            response = get_data(
                name=name.strip(),
                postal_code=postal_code.strip(),
                city=city.strip() if city else None,
                state_code=state_code.strip() if state_code else None,
                street_line_1=street_line_1.strip() if street_line_1 else None,
                street_line_2=street_line_2.strip() if street_line_2 else None,
                other_info = other_info.strip() if other_info else None
            )
            # Display response
            st.markdown(f"### Response:\n{response}")

if __name__ == "__main__":
    main()