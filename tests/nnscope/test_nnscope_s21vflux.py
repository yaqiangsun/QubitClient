# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/10/20 18:24:01
########################################################################

import json
import os
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.scope.utils.data_parser import load_npy_file
from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName
from qubitclient.nnscope.utils.data_parser import load_npz_file
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType
from qubitclient.nnscope.utils.data_convert import convert_spectrum_npy2npz,convert_spectrum_dict2npz
from qubitclient.draw.pltmanager import QuantumPlotPltManager  #using matplotlib draw NPY/NPZ data
from qubitclient.draw.plymanager import QuantumPlotPlyManager #using plotly draw NPY/NPZ data



def send_s21vflux_npy_to_server(dir_path = None):
    # get all file in dir
    savenamelist=[]
    file_names = os.listdir(dir_path)
    
    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npy'):
            savenamelist.append(os.path.splitext(file_name)[0])
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    if len(file_path_list) == 0:
        return
    
    client = QubitNNScopeClient()

    dict_list = []
    for file_path in file_path_list:
        content = load_npy_file(file_path)
        # content = content[0]
        dict_list.append(content)  
    
    response = client.request(file_list=dict_list,task_type=NNTaskName.S21VSFLUX,curve_type=CurveType.AUTO)
    # 2.从文件路径直接加载
    # response = client.request(file_list=[file_path],task_type=NNTaskName.S21VSFLUX,curve_type=CurveType.COSINE)
    threshold = 0.1
    results = client.get_result(response, threshold=threshold, task_type=NNTaskName.S21VSFLUX.value)

    ply_plot_manager = QuantumPlotPlyManager()
    plt_plot_manager = QuantumPlotPltManager()

    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        # write result to json
        json_path = f'./tmp/result_json/{NNTaskName.S21VSFLUX.value}_{savenamelist[idx]}.json'
        content = {"params_list": result["params_list"], "linepoints_list": result["linepoints_list"]}
        with open(json_path, 'w') as f:
            json.dump(content, f)
                    
        save_path_prefix = f"./tmp/client/result_{NNTaskName.S21VSFLUX.value}_{savenamelist[idx]}"
        save_path_png = save_path_prefix + ".png"
        save_path_html = save_path_prefix + ".html"
        
        ply_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=NNTaskName.S21VSFLUX.value,
            save_path=save_path_html,
            result=result,
            dict_param=dict_param
        )

        plt_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=NNTaskName.S21VSFLUX.value,
            save_path=save_path_png,
            result=result,
            dict_param=dict_param
        )

    print(results)



def main():
    base_dir = "tmp/yaqiangsun/qubit_examples/s21vsflux"
    send_s21vflux_npy_to_server(base_dir)


if __name__ == "__main__":
    main()