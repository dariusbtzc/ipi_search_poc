# Follow below steps for setting up project

- Open terminal in PyCharm / VSCode
- `cd <project>/<folder>`
- `python3 -m venv env`
- `source env/bin/activate`
- `pip3 install --upgrade pip setuptools`
- `pip3 install -r requirements.txt`
- gcloud auth application-default login
- go to gcp cloud shell execute this `gcloud auth print-access-token` and copy it to main.py > bearer variable token
- `streamlit run main.py`

# Reference code
Google Vertex Search API: https://cloud.google.com/generative-ai-app-builder/docs/multi-turn-search
Streamlit API: https://blog.streamlit.io/create-a-search-engine-with-streamlit-and-google-sheets/