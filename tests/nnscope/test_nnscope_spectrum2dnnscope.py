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

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName
from qubitclient.nnscope.utils.data_parser import load_npz_file
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType
from qubitclient.nnscope.utils.data_convert import convert_spectrum_npy2npz,convert_spectrum_dict2npz
from qubitclient.draw.pltmanager import QuantumPlotPltManager  #using matplotlib draw NPY/NPZ data
from qubitclient.draw.plymanager import QuantumPlotPlyManager #using plotly draw NPY/NPZ data


def send_spectrum2dnnscope_npz_to_server(url, api_key,dir_path = "data/33137"):

    # get all file in dir
    file_names = os.listdir(dir_path)
    savename = os.path.basename(dir_path)


    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npy') or file_name.endswith('.npz'):
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    if len(file_path_list)==0:
        return

    client = QubitNNScopeClient(url=url,api_key=api_key)

    dict_list = []
    for file_path in file_path_list:
        content = load_npz_file(file_path)
        dict_list.append(content)

    #使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    response = client.request(file_list=dict_list,task_type=NNTaskName.SPECTRUM2D,curve_type=CurveType.COSINE)
    # 从文件路径直接加载
    # response = client.request(file_list=file_path_list,task_type=NNTaskName.SPECTRUM2D,curve_type=CurveType.COSINE)
    results = client.get_result(response=response)
    threshold = 0.5
    results_filtered = client.get_filtered_result(response,threshold,NNTaskName.SPECTRUM2D.value)

    save_path_prefix = f"./tmp/client/result_{NNTaskName.SPECTRUM2D.value}_{savename}"
    save_path_png = save_path_prefix + ".png"
    save_path_html = save_path_prefix + ".html"
    plot_manager = QuantumPlotPlyManager()
    plot_manager.plot_quantum_data(
        data_type='npz',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_path=save_path_html,
        results=results_filtered,
        dict_list=dict_list,
        file_names = file_names
    )
    plot_manager = QuantumPlotPltManager()
    plot_manager.plot_quantum_data(
        data_type='npz',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_path=save_path_png,
        results=results_filtered,
        dict_list=dict_list,
        file_names=file_names
    )
    # print(results)


def send_spectrum2dnnscope_npy_to_server(url, api_key,file_path = "/home/sunyaqiang/work/QubitClient/tmp/npyfile/tmp0bf97fdf.py_1536.npy"):

    # dict_list, name_list = convert_spectrum_npy2npz(file_path)
    base_name = os.path.basename(file_path)

    # 分割文件名和扩展名，返回文件名部分
    savename = os.path.splitext(base_name)[0]
    client = QubitNNScopeClient(url=url,api_key=api_key)
    
    # 1.使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    import numpy as np
    data_ndarray = np.load(file_path, allow_pickle=True)
    # data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
    response = client.request(file_list=[data_ndarray],task_type=NNTaskName.SPECTRUM2D,curve_type=CurveType.COSINE)
    # 2.从文件路径直接加载
    # response = client.request(file_list=[file_path],task_type=NNTaskName.SPECTRUM2D,curve_type=CurveType.COSINE)
    results = client.get_result(response=response)
    threshold = 0.5
    results_filtered = client.get_filtered_result(response, threshold, NNTaskName.SPECTRUM2D.value)
    save_path_prefix = f"./tmp/client/result_{NNTaskName.SPECTRUM2D.value}_{savename}"
    save_path_png = save_path_prefix + ".png"
    save_path_html = save_path_prefix + ".html"
    plot_manager = QuantumPlotPlyManager()
    plot_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_path=save_path_html,
        results=results_filtered,
        data_ndarray=data_ndarray
    )

    plot_manager = QuantumPlotPltManager()
    plot_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_path=save_path_png,
        results=results_filtered,
        data_ndarray=data_ndarray
    )

    # print(results)






def main():
    from config import API_URL, API_KEY

    # 1. npz file.
    # base_dir = "data/1829"
    # send_spectrum2dnnscope_npz_to_server(API_URL, API_KEY, base_dir)
    # 2. npy file.
    file_path = "tmp/data/spectrum2d/tmpb5c7f62d.py_311.npy"
    send_spectrum2dnnscope_npy_to_server(API_URL, API_KEY, file_path)



if __name__ == "__main__":
    main()