import pandas as pd


def json_to_pandas(result_ls):
    """
    Converts JSON search results to a pandas DataFrame.
    
    Parameters:
    - result_ls: A list of dictionaries.
    
    Returns:
    - A pandas DataFrame.
    """
    
    data_structured_json = {
        'extracted_answer_1': [],
        'display_link': [],
        'title': [],
        'link': []
    }

    for _, result in enumerate(result_ls):
        struct_data = result['document']['derivedStructData']

        extracted_answer_1 = struct_data['extractive_answers'][0]['content']
        display_link = struct_data.get('displayLink', '')
        title = struct_data['title']
        link = struct_data['link']

        data_structured_json['extracted_answer_1'].append(extracted_answer_1)
        data_structured_json['display_link'].append(display_link)
        data_structured_json['title'].append(title)
        data_structured_json['link'].append(link)

    return pd.DataFrame(data_structured_json)
