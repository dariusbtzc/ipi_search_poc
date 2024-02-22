# Import libraries
import streamlit as st
from search_request import search
from utils import json_to_pandas

# Page setup
st.set_page_config(page_title="Customize Search Engine")
st.title("IPI Tech Solutions Search Engine")

# Use a text_input to get the keywords to filter the dataframe
search_query = st.text_input("Search Tech Offers", value="")

project_id = "external-poc-ipi"
web_data_store_id = "ipi-tech-offers-webpages_1707807506408"
pdf_data_store_id = "ipi-tech-offers-pdfs_1707298107544"
bearer_token = "ya29.a0AfB_byCcPfgHV6AnAdfwZQPnT3lKwEQkcIkxaLLPgqWvoEZ0cHG2Mv5Z9686ZDTeozxmQTL_rWzZcaPaoOzFD0GCCpyKuSQkiQmwdEppqfk7QgdPQes0F9TJYHoqSC6HLQc7mu4G_OC3UMyLKZcGa42N7GuTU4IWd_6VTJjBGbfk7xsEaNJL3_03d99ulsREUK9k71Xev7NZLXoigO9G14FlejVlXUmKvWdUbtgr9TORff5abJ_3kNd9Yg7YdcPj0upfQvD14g5TshWcxmEpVc7cz_T5mIa2DHKzdVE2S44S3L0x89kPgKdoInwj4Df5P1HCn4-lGYbzspEtXn_VMCZ4a96elbhr-yVZEIHmM0BDDKGtpCMQyaBe5-cRvrXjIEcsUVQq1X-eqqmoU7TgwHZBQKDXh-vkaCgYKAZwSARASFQHGX2MiKU0RMLwE-SffbuxwSfa5pQ0423"


web_response = search(web_data_store_id, search_query, bearer_token)
pdf_response = search(pdf_data_store_id, search_query, bearer_token)
try:
    web_results = json_to_pandas(web_response['results'])
    pdf_results = json_to_pandas(pdf_response['results'])


    if search_query:
        st.header('Web Page Search Summary')
        st.write(web_response['summary']['summaryText'])
        st.header('PDF Search Summary')
        st.write(pdf_response['summary']['summaryText'])

        tab1, tab2 = st.tabs(["Web Search Results", "PDF Search Results"])
        with tab1:
            st.header('Web Search Results')
            for n_row, row in web_results.iterrows():
                st.markdown(f"__{row['title']}__")
                st.markdown(f"{row['extracted_answer_1']}")
                st.markdown(f"**{row['link']}**")

        with tab2:
            st.header('PDF Search Results')
            for n_row, row in pdf_results.iterrows():
                st.markdown(f"__{row['title']}__")
                st.markdown(f"*{row['extracted_answer_1']}*")
                st.markdown(f"**{row['link']}**")
except:
    st.write(web_response)
    st.write(pdf_response)
    # st.write(web_results)
    # st.write(pdf_results)
# response = search_sample(project_id, project_id, web_data_store_id, search_query)


# curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" \
# -H "Content-Type: application/json" \
# "https://discoveryengine.googleapis.com/v1alpha/projects/105450411481/locations/global/collections/default_collection/dataStores/ipi-tech-offers-pdfs_1707298107544/conversations/-:converse" \
# -d '{"query":{"input":"<QUERY>"},"summarySpec":{"summaryResultCount":5,"modelPromptSpec":{"preamble":"Given the conversation between a user and a helpful assistant and some search results, create a final answer for the assistant. The answer should use all relevant information from the search results, not introduce any additional information, and use the same words as the search results as much as possible. The assistant's answer should be brief, no more than 5 sentences. Also, whenever necessary, use the actual company name \"IPI\" instead of a placeholder name such as \"The Company\"."},"ignoreAdversarialQuery":true,"includeCitations":true}}'


# # Another way to show the filtered results
# # Show the cards
# N_cards_per_row = 3
# if text_search:
#     for n_row, row in df_search.reset_index().iterrows():
#         i = n_row%N_cards_per_row
#         if i==0:
#             st.write("---")
#             cols = st.columns(N_cards_per_row, gap="large")
#         # draw the card
#         with cols[n_row%N_cards_per_row]:
#             st.caption(f"{row['Evento'].strip()} - {row['Lugar'].strip()} - {row['Fecha'].strip()} ")
#             st.markdown(f"**{row['Autor'].strip()}**")
#             st.markdown(f"*{row['Título'].strip()}*")
#             st.markdown(f"**{row['Video']}**")
