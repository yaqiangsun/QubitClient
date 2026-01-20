import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient import QubitScopeClient
from qubitclient import TaskName

from qubitclient.scope.utils.data_parser import load_npy_file

def transform_t1fit_npy_and_processed_data(url, api_key, dict_list):
    client = QubitScopeClient(url=url, api_key=api_key)
    response = client.request(file_list=dict_list, task_type=TaskName.T1FIT)
    print(response)

    if hasattr(response, 'parsed'):
        response_data = response.parsed
    elif isinstance(response, dict):
        response_data = response
    else:
        response_data = {}

    results = response_data.get("results")
    trans_all_npy = []

    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        data = dict_param.item()
        image = data["image"]
        q_list = image.keys()

        params_list = result.get('params_list', [])
        r2_list = result.get('r2_list', [])
        fit_data_list = result.get('fit_data_list', [])
        status_global = result.get('status', 'failed')

        trans_single_npy = []

        for q_idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[0]
            amp = image_q[1]

            data_list = [[xi.item(), ai.item()] for xi, ai in zip(x, amp)]

            label = {}
            if q_idx < len(params_list):
                A, T1, B = params_list[q_idx]
                label["params_list"] = [A, T1, B]
                label["r2"] = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                label["fit_data_list"] = fit_data_list[q_idx] if q_idx < len(fit_data_list) else []
                label["status"] = "success" if status_global == "success" else "failed"
            else:
                label["params_list"] = [0.0, 0.0, 0.0]
                label["r2"] = 0.0
                label["fit_data_list"] = []
                label["status"] = "failed"

            trans_single_npy.append({
                "data": data_list,
                "label": [label]
            })

        trans_all_npy.append(trans_single_npy)

    return trans_all_npy


def main():
    from config import API_URL, API_KEY
    base_dir = "./data/t1_1d_test"
    file_names = os.listdir(base_dir)
    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npy'):
            file_path = os.path.join(base_dir, file_name)
            file_path_list.append(file_path)
    if len(file_path_list) == 0:
        return

    dict_list = []
    for file_path in file_path_list:
        content = load_npy_file(file_path)
        dict_list.append(content)

    trans_all_npy = transform_t1fit_npy_and_processed_data(API_URL, API_KEY, dict_list)

if __name__ == "__main__":
    main()