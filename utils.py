import pandas as pd


def get_scoring(response):
    return response['summary']['scores']


def json_to_pandas(result_ls, score_ls=None):
    data_structured_json = {
        'extracted_answer_1': [],
        'display_link': [],
        'title': [],
        'link': [],
        'score': []
    }

    for idx, result in enumerate(result_ls):
        struct_data = result['document']['derivedStructData']

        extracted_answer_1 = struct_data['extractive_answers'][0]['content']
        display_link = struct_data.get('displayLink', '')
        title = struct_data['title']
        link = struct_data['link']

        data_structured_json['extracted_answer_1'].append(extracted_answer_1)
        data_structured_json['display_link'].append(display_link)
        data_structured_json['title'].append(title)
        data_structured_json['link'].append(link)

        try:
            data_structured_json['score'].append(score_ls[idx] if score_ls else 0)
        except IndexError:
            data_structured_json['score'].append(0)

    return pd.DataFrame(data_structured_json)
