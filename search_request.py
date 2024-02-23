import requests


# TODO: Find a dynamical way for authentication
def build_headers(bearer_token):
    """
    Constructs the headers needed for the API request.
    
    Parameters:
    - bearer_token: A string representing the OAuth 2.0 bearer token for authentication.
    
    Returns:
    - A dictionary with Authorization and Content-Type headers.
    """

    headers = {
        'Authorization': 'Bearer ' + bearer_token,
        'Content-Type': 'application/json',     # Content type set to JSON
    }

    return headers


def build_json_data(datastore_id, query, context = None):
    """
    Creates the JSON payload for the search request.
    
    Parameters:
    - datastore_id: The identifier of the data store to search against.
    - query: The search query string.
    
    Returns:
    - A dictionary representing the JSON payload for the request.
    """

    json_data = {
        'servingConfig': f'projects/external-poc-ipi/locations/global/collections/default_collection/dataStores/{datastore_id}/servingConfigs/default_search',
        'query': query,
        'pageSize': '5',                        # Limit the number of results to 5
        'offset': '0',                          # Start at the beginning of the results
        'params': {
            'searchType': '0',                  
        },
        'contentSearchSpec': {                  # Configuration for summary
            'summarySpec': {
                'summaryResultCount': 5,
                'includeCitations': True,
                'ignoreAdversarialQuery': True,
                'ignoreNonSummarySeekingQuery': True
            },
            'extractiveContentSpec': {          # Configuration for extractive answer
                'maxExtractiveAnswerCount': 1,  
                'returnExtractiveSegmentScore': True
            }
        }
    }

    # # Add the context to the payload, if present
    # if context:
    #     json_data['context'] = context 

    return json_data


def build_url(datastore_id):
    """
    Constructs the API request URL.
    
    Parameters:
    - datastore_id: The identifier of the data store being queried.
    
    Returns:
    - A string with the fully constructed URL for the search request.
    """

    return f'https://discoveryengine.googleapis.com/v1beta/projects/external-poc-ipi/locations/global/collections/default_collection/dataStores/{datastore_id}/servingConfigs/default_search:search'


def curl_request(url, headers, json_data):
    """
    Sends a POST request to the API.
    
    Parameters:
    - url: The URL to which the request is sent.
    - headers: The headers for the request, including authorization.
    - json_data: The JSON payload of the request.
    
    Returns:
    - The response from the API as a requests.Response object.
    """

    response = requests.post(
        url = url,
        headers = headers,
        json = json_data
    )

    return response


def search(datastore_id, query, bearer_token, context = None):
    """
    Main function to perform a search operation.
    
    Parameters:
    - datastore_id: The data store to search against.
    - query: The search query string.
    - bearer_token: The OAuth 2.0 bearer token for authentication.
    
    Returns:
    - The parsed JSON response from the search API.
    """

    # Build the URL, headers and JSON data for the search request
    url = build_url(datastore_id)
    headers = build_headers(bearer_token)
    json_data = build_json_data(datastore_id, query)
    
    # Send the search request and return the JSON response
    response = curl_request(url, headers, json_data)

    return response.json()