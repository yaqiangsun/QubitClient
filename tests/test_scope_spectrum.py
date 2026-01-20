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


def send_spectrum_npy_to_server(url, api_key, dir_path="data/33137"):
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
    response = client.request(file_list=dict_list, task_type=TaskName.SPECTRUM)

    # === 解析结果并绘图（每个文件单独生成 HTML）===

    # 1. 解析服务器返回
    if hasattr(response, 'parsed'):
        response_data = response.parsed
    elif isinstance(response, dict):
        response_data = response
    else:
        response_data = {}
    results = response_data.get("results")
    ply_plot_manager = QuantumPlotPlyManager()
    plt_plot_manager = QuantumPlotPltManager()
    for idx, (result, item) in enumerate(zip(results, dict_list)):

        if isinstance(result, dict) and \
        result.get('status') == 'failed' and \
        result.get('error') == "'image'":
            print(f"the task of idx {idx} failed: No image data available")
            continue  # 继续下一次循环
        save_path_prefix = f"./tmp/client/result_{TaskName.SPECTRUM.value}_{savenamelist[idx]}"
        save_path_png = save_path_prefix + ".png"
        save_path_html = save_path_prefix + ".html"
        # 正常执行绘图任务
        try:
            plt_plot_manager.plot_quantum_data(
                data_type='npy',
                task_type=TaskName.SPECTRUM.value,
                save_path=save_path_png,
                result=result,
                dict_param=item
            )
            ply_plot_manager.plot_quantum_data(
                data_type='npy',
                task_type=TaskName.SPECTRUM.value,
                save_path=save_path_html,
                result=result,
                dict_param=item
            )
        except Exception as e:
            print(f"idx {idx} failed: {str(e)}")
            continue  


def main():
    from config import API_URL, API_KEY

    base_dir = "./data"
    send_spectrum_npy_to_server(API_URL, API_KEY, base_dir)


if __name__ == "__main__":
    main()