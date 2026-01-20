# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/10/20 18:24:01
########################################################################

import os
import sys

# 获取当前文件的绝对路径，向上两层就是项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient import QubitScopeClient
from qubitclient import TaskName

from qubitclient.scope.utils.data_parser import load_npy_file
from qubitclient.draw.pltmanager import QuantumPlotPltManager  # using matplotlib draw NPY/NPZ data
from qubitclient.draw.plymanager import QuantumPlotPlyManager  # using plotly draw NPY/NPZ data

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def send_s21vflux_npy_to_server(url, api_key, dir_path="data/33137"):
    # get all file in dir
    savenamelist = []
    file_names = os.listdir(dir_path)

    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npy'):
            savenamelist.append(os.path.splitext(file_name)[0])
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    if len(file_path_list) == 0:
        return

    client = QubitScopeClient(url=url, api_key=api_key)

    dict_list = []
    for file_path in file_path_list:
        content = load_npy_file(file_path)
        dict_list.append(content)

        # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    response = client.request(file_list=dict_list, task_type=TaskName.S21VFLUX)
    print(response)

    response_data = client.get_result(response)

    threshold = 0.5
    response_data_filtered = client.get_filtered_result(response,threshold,TaskName.S21VFLUX.value)

    results = response_data_filtered.get("results")

    ply_plot_manager = QuantumPlotPlyManager()
    plt_plot_manager = QuantumPlotPltManager()
    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        save_path_prefix = f"./tmp/client/result_{TaskName.S21VFLUX.value}_{savenamelist[idx]}"
        save_path_png = save_path_prefix + ".png"
        save_path_html = save_path_prefix + ".html"
        plt_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=TaskName.S21VFLUX.value,
            save_path=save_path_png,
            result=result,
            dict_param=dict_param
        )
        ply_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=TaskName.S21VFLUX.value,
            save_path=save_path_html,
            result=result,
            dict_param=dict_param
        )


def main():
    from config import API_URL, API_KEY

    base_dir = "./tmp/s21vlux"
    send_s21vflux_npy_to_server(API_URL, API_KEY, base_dir)


if __name__ == "__main__":
    main()