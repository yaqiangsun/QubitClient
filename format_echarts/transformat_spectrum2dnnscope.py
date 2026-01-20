# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/10/20 18:24:01
########################################################################

import os
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName
from qubitclient.nnscope.utils.data_parser import load_npz_file
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType
from qubitclient.nnscope.utils.data_convert import convert_spectrum_npy2npz, convert_spectrum_dict2npz
from qubitclient.draw.pltmanager import QuantumPlotPltManager  # using matplotlib draw NPY/NPZ data
from qubitclient.draw.plymanager import QuantumPlotPlyManager  # using plotly draw NPY/NPZ data

import numpy as np



def transform_spectrum2dnnscope_npz_and_processed_data(url, api_key, dict_list):
    # get all file in dir

    client = QubitNNScopeClient(url=url, api_key=api_key)



    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    response = client.request(file_list=dict_list, task_type=NNTaskName.SPECTRUM2D, curve_type=CurveType.COSINE)
    # 从文件路径直接加载
    # response = client.request(file_list=file_path_list,task_type=NNTaskName.SPECTRUM2D,curve_type=CurveType.COSINE)
    results = client.get_result(response=response)

    trans_all_npz=[]
    for idx in range(len(dict_list)):
        data = dict_list[idx]
        bias = data['bias']
        frequency = data['frequency']
        iq_avg = data['iq_avg']


        bias_grid, frequency_grid = np.meshgrid(bias, frequency)
        data_list = np.column_stack([
            bias_grid.ravel(),  # 横坐标x (电压)
            frequency_grid.ravel(),  # 纵坐标y (频率)
            iq_avg.ravel()  # 值s (S参数)
        ]).tolist()

        result = results[idx]
        linepoints_list = result['linepoints_list']
        confidence_list = result['confidence_list']

        lable_list = []
        line_sum = 0
        for i in range(len(linepoints_list)):
            line_sum += 1
            lable_list.append({
                "name": f"Line{line_sum}",
                "conf": confidence_list[i],
                "data": linepoints_list[i]
            })

        trans_all_npz.append({
            "data": data_list,
            "label": lable_list
        })
    return trans_all_npz


def transform_spectrum2dnnscope_npy_and_processed_data(url, api_key,data_ndarray):


    client = QubitNNScopeClient(url=url, api_key=api_key)

    # 1.使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    # data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
    response = client.request(file_list=[data_ndarray], task_type=NNTaskName.SPECTRUM2D, curve_type=CurveType.COSINE)
    # 2.从文件路径直接加载
    # response = client.request(file_list=[file_path],task_type=NNTaskName.SPECTRUM2D,curve_type=CurveType.COSINE)
    results = client.get_result(response=response)
    data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
    data_dict = data_dict['image']
    q_list = data_dict.keys()
    trans_single_npy=[]
    for idx, q_name in enumerate(q_list):
        image_q = data_dict[q_name]
        bias = image_q[1]
        frequency = image_q[2]
        iq_avg = np.abs(image_q[0])
        bias_grid, frequency_grid = np.meshgrid(bias, frequency)
        data_list = np.column_stack([
            bias_grid.ravel(),  # 横坐标x (电压)
            frequency_grid.ravel(),  # 纵坐标y (频率)
            iq_avg.ravel()  # 值s (S参数)
        ]).tolist()

        result = results[idx]
        linepoints_list = result['linepoints_list']
        confidence_list = result['confidence_list']

        lable_list = []
        line_sum = 0
        for i in range(len(linepoints_list)):
            line_sum += 1
            lable_list.append({
                "name": f"Line{line_sum}",
                "conf": confidence_list[i],
                "data": linepoints_list[i]
            })

        trans_single_npy.append({
            "data": data_list,
            "label": lable_list
        })
    return trans_single_npy

def main():
    from config import API_URL, API_KEY

    # # 1. npz file.
    base_dir = "data/1829"
    file_names = os.listdir(base_dir)
    savename = os.path.basename(base_dir)

    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npy') or file_name.endswith('.npz'):
            file_path = os.path.join(base_dir, file_name)
            file_path_list.append(file_path)
    if len(file_path_list) == 0:
        return
    dict_list = []
    for file_path in file_path_list:
        content = load_npz_file(file_path)
        dict_list.append(content)

    trans_all_npz = transform_spectrum2dnnscope_npz_and_processed_data(API_URL, API_KEY, dict_list)


    # 2. npy file.
    file_path = "/media/lining/d7a0fb11-79c9-4c24-8500-1384fde9fe6d/projects/quantum/client_1101/QubitClient_1101/tests/tmp/npyfile/tmp6d08e0e9.py_7157.npy"
    # dict_list, name_list = convert_spectrum_npy2npz(file_path)
    base_name = os.path.basename(file_path)
    data_ndarray = np.load(file_path, allow_pickle=True)

    trans_single_npy = transform_spectrum2dnnscope_npy_and_processed_data(API_URL, API_KEY, data_ndarray)


if __name__ == "__main__":
    main()