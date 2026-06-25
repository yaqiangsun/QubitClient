# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient import QubitScopeClient, TaskName
from qubitclient.draw.pltmanager import QuantumPlotPltManager
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.scope.utils.data_parser import load_npy_file


def send_spinecho_npy_to_server(url, api_key, dir_path="data/spin_echo", batch_size=5):
    savenamelist = []
    file_names = os.listdir(dir_path)

    file_path_list = []
    for file_name in file_names:
        if file_name.endswith(".npy"):
            savenamelist.append(os.path.splitext(file_name)[0])
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    if len(file_path_list) == 0:
        return

    client = QubitScopeClient(url=url, api_key=api_key)
    total = len(file_path_list)

    ply_plot_manager = QuantumPlotPlyManager()
    plt_plot_manager = QuantumPlotPltManager()

    for start_idx in range(0, total, batch_size):
        end_idx = min(start_idx + batch_size, total)
        batch_paths = file_path_list[start_idx:end_idx]
        batch_savenames = savenamelist[start_idx:end_idx]

        print(f"Processing batch [{start_idx + 1}-{end_idx}/{total}]")

        dict_list = []
        for file_path in batch_paths:
            content = load_npy_file(file_path)
            dict_list.append(content)

        response = client.request(file_list=dict_list, task_type=TaskName.SPINECHO)
        print(response)

        response_data = client.get_result(response)
        threshold = -1
        response_data_filtered = client.get_filtered_result(
            response, threshold, TaskName.SPINECHO.value
        )

        results = response_data_filtered.get("results")

        for idx_in_batch, (result, dict_param) in enumerate(zip(results, dict_list)):
            global_idx = start_idx + idx_in_batch
            original_file = file_names[global_idx]

            if isinstance(result, dict) and result.get("status") == "failed":
                print(f"{original_file} failed: No image data available")
                continue

            qubit_results = [
                v for k, v in result.items()
                if k != "status" and isinstance(v, dict) and v.get("x")
            ] if isinstance(result, dict) else []
            if not qubit_results:
                print(f"{original_file} failed: No fit data available")
                continue

            save_path_prefix = (
                f"./tmp/client/result_{TaskName.SPINECHO.value}_"
                f"{batch_savenames[idx_in_batch]}"
            )
            save_path_png = save_path_prefix + ".png"
            save_path_html = save_path_prefix + ".html"

            plt_plot_manager.plot_quantum_data(
                data_type="npy",
                task_type=TaskName.SPINECHO.value,
                save_path=save_path_png,
                result=result,
                dict_param=dict_param,
            )
            ply_plot_manager.plot_quantum_data(
                data_type="npy",
                task_type=TaskName.SPINECHO.value,
                save_path=save_path_html,
                result=result,
                dict_param=dict_param,
            )
            print(
                f"Generated: {os.path.basename(save_path_html)} "
                f"and {os.path.basename(save_path_png)}"
            )


def main():
    from config import API_URL, API_KEY
    base_dir = "tmp/yaqiangsun/qubit_examples/spinecho"
    send_spinecho_npy_to_server(API_URL, API_KEY, base_dir, batch_size=1)


if __name__ == "__main__":
    main()
