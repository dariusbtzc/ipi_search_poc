import requests

def build_headers(bearer_token):
    # TODO : find out dynamical ways of authentication
    headers = {
        'Authorization': 'Bearer ' + bearer_token,
        'Content-Type': 'application/json',
    }
    return headers


def build_json_data(data_store_id,query):
    # TODO explore more settings. e.g. follow up quesitions
    # https://cloud.google.com/generative-ai-app-builder/docs/multi-turn-search
    json_data = {
        'servingConfig': f'projects/external-poc-ipi/locations/global/collections/default_collection/dataStores/{data_store_id}/servingConfigs/default_search',
        'query': query,
        'pageSize': '5',
        'offset': '0',
        'params': {
            'searchType': '0',
        },
        'contentSearchSpec': {
            'summarySpec': {
                'summaryResultCount': 3,
            },
            'extractiveContentSpec': {
                'maxExtractiveAnswerCount': 1,
            },
        },
    }
    return json_data


def build_url(datastore):
    return f'https://discoveryengine.googleapis.com/v1beta/projects/external-poc-ipi/locations/global/collections/default_collection/dataStores/{datastore}/servingConfigs/default_search:search'


def curl_request(url, headers, json_data):
    response = requests.post(
        url=url,
        headers=headers,
        json=json_data
    )
    return response


def search(datastore, query, bearer_token):
    url = build_url(datastore)
    headers = build_headers(bearer_token)
    json_data = build_json_data(datastore, query)
    response = curl_request(url, headers, json_data)
    return response.json()


# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
# data = '{\n"servingConfig": "projects/external-poc-ipi/locations/global/collections/default_collection/dataStores/ipi-tech-offers-webpages_1707807506408/servingConfigs/default_search",\n"query": "waste",\n"pageSize": "5",\n"offset": "0",\n"params": {"searchType": "0"},\n"contentSearchSpec":  {\n   "summarySpec":\n   {\n     "summaryResultCount": 3\n   },\n   "extractiveContentSpec": { "maxExtractiveAnswerCount" : 1}\n }\n}'
# response = requests.post(
#    'https://discoveryengine.googleapis.com/v1beta/projects/external-poc-ipi/locations/global/collections/default_collection/dataStores/ipi-tech-offers-webpages_1707807506408/servingConfigs/default_search:search',
#    headers=headers,
#    data=data,
# )
