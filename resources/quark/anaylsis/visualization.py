# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 12:00:26
########################################################################


import numpy as np
import matplotlib.pyplot as plt

from qubitclient.draw.pltmanager import QuantumPlotPltManager
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient import TaskName,NNTaskName

from datetime import date
from pathlib import Path
import os
import logging
from .config import API_URL,API_KEY,ENABLE_API
from .wrapper_handler import handle_exceptions, control_api_execution

from .format import optpipulse_convert

def plot_template(data,results,save_path,task_type=TaskName.S21PEAK):

    if type(results)==dict:
        results = results.get("results")
    image = data
    dict_list = [np.array(image)]

    ply_plot_manager = QuantumPlotPlyManager()
    plt_plot_manager = QuantumPlotPltManager()
    print("plotting ai image...")
    print(save_path)
    fig_list = []

    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        save_path_png = str(save_path)
        save_path_html = save_path_png.replace("png",".html")
        fig_plt = plt_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=task_type.value,
            save_path=save_path_png,
            result=result,
            dict_param=dict_param
        )
        fig_list.append(fig_plt)
        fig_ply = ply_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=task_type.value,
            save_path=save_path_html,
            result=result,
            dict_param=dict_param
        )
    logging.info(f"Saving ai image to:{save_path}")
    return fig_list

def plot_optpipulse(data,results,save_path):
    data = optpipulse_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.OPTPIPULSE)
    return fig_list
