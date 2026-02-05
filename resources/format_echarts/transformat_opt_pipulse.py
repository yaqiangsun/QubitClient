import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient import QubitScopeClient
from qubitclient import TaskName

from qubitclient.scope.utils.data_parser import load_npy_file

def transform_opt_pipulse_npy_and_processed_data(url, api_key, dict_list):
    client = QubitScopeClient(url=url, api_key=api_key)
    response = client.request(file_list=dict_list, task_type=TaskName.OPTPIPULSE)
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

        peaks_list = result['params']
        confs_list = result['confs']
        status_global = result.get('status', 'failed')

        trans_single_npy = []

        for q_idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            waveforms = image_q[0]
            x = image_q[1]

            n_waveforms = waveforms.shape[0]
            n_points = len(x)

            data_list = []
            for i in range(n_points):
                row = [waveforms[w, i].item() for w in range(n_waveforms)]
                row.append(x[i].item())
                data_list.append(row)

            label_list = []
            if q_idx < len(peaks_list) and len(peaks_list[q_idx]) > 0:
                for point_idx, (peak_x, conf) in enumerate(zip(peaks_list[q_idx], confs_list[q_idx]), 1):
                    label_list.append({
                        "name": f"Point{point_idx}",
                        "peak": peak_x,
                        "conf": conf,
                        "status": "success" if status_global == "success" else "failed"
                    })

            trans_single_npy.append({
                "data": data_list,
                "label": label_list
            })

        trans_all_npy.append(trans_single_npy)

    return trans_all_npy

def main():
    from config import API_URL, API_KEY
    base_dir = "./data/ramsey_test"
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

    trans_all_npy = transform_opt_pipulse_npy_and_processed_data(API_URL, API_KEY, dict_list)


if __name__ == "__main__":
    main()