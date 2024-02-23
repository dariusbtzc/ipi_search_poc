# Import libraries
import streamlit as st
from search_request import search
from utils import json_to_pandas


# Page setup
st.set_page_config(page_title = "IPI Search Engine")
st.title("IPI Tech Solutions Search Engine")


# # Initialize or update the search context in Streamlit's session state
# if 'search_context' not in st.session_state:
#     st.session_state['search_context'] = None


# Initialize search and summary histories in Streamlit's session state
if 'search_history' not in st.session_state:
    st.session_state['search_history'] = {'web': [], 'pdf': []}
if 'summary_history' not in st.session_state:
    st.session_state['summary_history'] = {'web': [], 'pdf': []}


# Text input field for users to enter their search query
search_query = st.text_input("Search Tech Offers:", value = "")


# Configuration variables for the project and data stores
project_id = "external-poc-ipi"
web_datastore_id = "ipi-tech-offers-webpages_1707807506408"
pdf_datastore_id = "ipi-tech-offers-pdfs_1707298107544"
bearer_token = "ya29.a0AfB_byDhUf2MZS-Qv3a1-ZtcUtiGTnqoQEyO4rYO6NUXsWTH6vsWsdgb58hv3Psmi5taOEbuiKfzPZAitZs456VpNy5bW0lfdjLwDTQjPBtQvJBTqV7aX1-PoCX9La_a5KUYzyERdw22PYn2baudJoxB3g4heTLU0knUPHH3zwpt9rnNutPCdL1To6-yOwHGeqtm4qvCfrEPuve5SJ2JRjxgCmDU6AaVYyO_k3cJcsKVPahT-MmpB_x4OIX-Zdxf-OM-5ZR2hheD8KAUFut4eBDkQFwjvT0GZUvLohouXU1g28QpWIvRurvC2aVoYyJMYqawiyze3R3cDAtGoBNqezUkqsJWU0OvdPH-XzdemnpM7JsBtitAxHCQP9Ht3_DXEv1rBXsCjrnRSuUDnKmrLwQy65STtyp-aCgYKAW8SARASFQHGX2Mii1xLgLdTuKgpLs8maHmgtA0423"


# Perform search operations for both web pages and PDFs data stores using the provided query and context
web_response = search(web_datastore_id, search_query, bearer_token)     # context: st.session_state['search_context']
pdf_response = search(pdf_datastore_id, search_query, bearer_token)     # context: st.session_state['search_context']
# st.write(web_response)
# st.write(pdf_response)


# # Update the context in the session state with the context from the responses if available
# if 'context' in web_response:
#     st.session_state['search_context'] = web_response.get('context', None)
# if 'context' in pdf_response and not st.session_state['search_context']:
#     st.session_state['search_context'] = pdf_response.get('context', None)


# Update history after each search
if search_query:

    # Update search history
    st.session_state['search_history']['web'].append(search_query)
    st.session_state['search_history']['pdf'].append(search_query)

    # Update summary history
    web_summary = web_response.get('summary', {}).get('summaryText', 'No summary available')
    pdf_summary = pdf_response.get('summary', {}).get('summaryText', 'No summary available')
    st.session_state['summary_history']['web'].append(web_summary)
    st.session_state['summary_history']['pdf'].append(pdf_summary)


# Display search and summary histories
with st.expander("Search History"):
    st.header("Web Search History")
    for i, (query, summary) in enumerate(zip(st.session_state['search_history']['web'], st.session_state['summary_history']['web']), start = 1):
        st.markdown(f"{i}. Query: `{query}`")
        st.markdown(f"   Summary: {summary}")

    st.header("PDF Search History")
    for i, (query, summary) in enumerate(zip(st.session_state['search_history']['pdf'], st.session_state['summary_history']['pdf']), start = 1):
        st.markdown(f"{i}. Query: `{query}`")
        st.markdown(f"   Summary: {summary}")


# Process and display the search results
try:

    # Convert search results to Pandas DataFrames for easier manipulation
    web_results = json_to_pandas(web_response['results'])
    pdf_results = json_to_pandas(pdf_response['results'])

    if search_query:
        
        # Add vertical space
        st.markdown("\n\n\n")

        # Display summaries for web and PDF search results
        st.header('Web Search Summary')
        st.write(web_response['summary']['summaryText'])
        st.header('PDF Search Summary')
        st.write(pdf_response['summary']['summaryText'])
        
        # Add vertical space
        st.markdown("\n\n\n")

        # Create tabs for web and PDF search results
        tab1, tab2 = st.tabs(["Web Search Results", "PDF Search Results"])
        with tab1:
            st.header('Web Search Results')

            # Iterate through web search results and display them
            for n_row, row in web_results.iterrows():
                st.markdown(f"**{row['title']}**")
                st.markdown(f"{row['extracted_answer_1']}")
                st.markdown(f"{row['link']}")
                
                # Add vertical space
                st.markdown("\n\n")

        with tab2:
            st.header('PDF Search Results')

            # Iterate through PDF search results and display them
            for n_row, row in pdf_results.iterrows():
                st.markdown(f"**{row['title']}**")
                st.markdown(f"{row['extracted_answer_1']}")
                st.markdown(f"*{row['link']}*")

                # Add vertical space
                st.markdown("\n\n")

except Exception as e:
    # If there's an error, display a message
    st.error(f"An error occurred: {e}")
    st.write(web_response)
    st.write(pdf_response)