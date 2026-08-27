import json
from dataclasses import asdict


def json_result(result_list: list):

    json_dict = {'target': '',
                 'intel': []}

    for i in result_list:
        if json_dict['target'] == '':
            json_dict['target'] = i.target

        json_data = asdict(i)
        del json_data['target']
        json_data['status'] = json_data['status'].value if json_data['status'] is not None else ''

        json_dict['intel'].append(json_data)

    return json_dict


def json_write(data_dict: dict):

    with open(f'results/result_{data_dict["target"]}.json', 'w') as file:
        json.dump(data_dict, file, indent= 4)

def json_execute(result_list: list):

    data = json_result(result_list)
    json_write(data)