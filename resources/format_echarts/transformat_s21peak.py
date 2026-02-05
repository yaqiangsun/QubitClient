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


def transform_s21peak_npy_and_processed_data(url, api_key, dict_list):
    savenamelist = []
    client = QubitScopeClient(url=url, api_key=api_key)
        # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    response = client.request(file_list=dict_list, task_type=TaskName.S21PEAK)
    print(response)

    # === 解析结果并绘图（每个文件单独生成 HTML）===
    # 1. 解析服务器返回
    if hasattr(response, 'parsed'):
        response_data = response.parsed
    elif isinstance(response, dict):
        response_data = response
    else:
        response_data = {}

    results = response_data.get("results")
    trans_all_npy=[]
    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        result = result
        data = dict_param.item()
        image = data["image"]
        q_list = image.keys()
        peaks_list = result['peaks']
        confs_list = result['confs']
        trans_single_npy=[]

        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[0]
            amp = image_q[1]
            phi = image_q[2]
            data_list = [[xi.item(), ai.item(), pi.item()] for xi, ai, pi in zip(x, amp, phi)]
            lable_list=[]
            point_sum=0
            for i in range(len(peaks_list[idx])):
                point_sum+=1
                lable_list.append({
                    "name":f"Point{point_sum}",
                    "conf":confs_list[idx][i],
                    "data":peaks_list[idx][i]
                })
            trans_single_npy.append({
                "data":data_list,
                "label":lable_list
            })
        trans_all_npy.append(trans_single_npy)
    return trans_all_npy


def main():
    from config import API_URL, API_KEY
    base_dir = "./tmp/s21_peak"
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
    trans_all_npy = transform_s21peak_npy_and_processed_data(API_URL, API_KEY, dict_list)  # trans_all_npy的数据格式参考format_s21vflux.json


if __name__ == "__main__":
    main()