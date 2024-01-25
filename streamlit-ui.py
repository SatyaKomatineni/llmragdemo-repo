import streamlit as st

#
#**************************************************
# Key elements
# 1. A form with a submit
# 2. Process text input
# 3. Write back what is entered so far
# 4. Rememebers with each web refresh the state
#**************************************************
#
def writeIntro():
    # Streamlit page layout
    st.title("Demo page")

    st.write("hello there")
    st.write("hello there")
    st.write("hello there")


def initialize_state():
    writeIntro()
    
    """Initialize the state variable."""
    if 'totalResponseText' not in st.session_state:
        st.session_state.totalResponseText = []

def writeOutput():
    # Display the accumulated text
    st.write("Accumulated Text:")
    for line in st.session_state.totalResponseText:
        st.write(line)


def process_input(input_text):
    """Append the input text to the totalResponseText state variable."""
    st.session_state.totalResponseText.append(input_text)

def main():
    """Main function to render the Streamlit page."""
    initialize_state()

    # Create a form
    with st.form(key='input_form'):
        text_input = st.text_input("Enter your text")
        submit_button = st.form_submit_button("Submit")

    # Process the form submission
    if submit_button and text_input:
        process_input(text_input)

    writeOutput()

#Kick it off
main()