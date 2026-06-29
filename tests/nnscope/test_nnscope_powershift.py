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

import os
import os
import sys
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName
from qubitclient.nnscope.utils.data_parser import load_npz_file
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType
from qubitclient.nnscope.utils.data_convert import convert_spectrum_npy2npz,convert_spectrum_dict2npz
from qubitclient.draw.pltmanager import QuantumPlotPltManager  # using matplotlib draw NPY/NPZ data
from qubitclient.draw.plymanager import QuantumPlotPlyManager # using plotly draw NPY/NPZ data
import logging
logging.getLogger().setLevel(logging.INFO)


def send_powershift_npy_to_server(file_path = None):

    # dict_list, name_list = convert_spectrum_npy2npz(file_path)
    base_name = os.path.basename(file_path)

    # 分割文件名和扩展名，返回文件名部分
    savename = os.path.splitext(base_name)[0]
    client = QubitNNScopeClient()
    
    # 1.使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    data_ndarray = np.load(file_path, allow_pickle=True)
    dict_list = [data_ndarray]
    response = client.request(file_list=dict_list,task_type=NNTaskName.POWERSHIFT)

    threshold = 0.7
    results = client.get_result(response, threshold=threshold, task_type=NNTaskName.POWERSHIFT.value)
    logging.info("results after get_result  : %s", results)

    save_path_prefix = f"./tmp/client/result_{NNTaskName.POWERSHIFT.value}_{savename}"
    save_path_png = save_path_prefix + ".png"
    save_path_html = save_path_prefix + ".html"

    plot_manager = QuantumPlotPlyManager()

    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        # html
        plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=NNTaskName.POWERSHIFT.value,
            save_path=save_path_html,
            result=result,
            dict_param=dict_param
        )

        plot_manager = QuantumPlotPltManager()
        # png
        plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=NNTaskName.POWERSHIFT.value,
            save_path=save_path_png,
            result=result,
            dict_param=dict_param
        )


def main():
    file_path = "tmp/yaqiangsun/qubit_examples/powershift/tmp71f11e2f.py_673.npy"
    send_powershift_npy_to_server(file_path)


if __name__ == "__main__":
    main()