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
from qubitclient import handle_exceptions, control_api_execution

from .format import optpipulse_convert,s21_convert,s21vsflux_convert,drag_convert,singleshot_convert,nnspectrum2d_convert,nns21vsflux_convert,spectrum2d_convert,t1fit_convert,t2fit_convert,rabicos_convert

def plot_template(data,results,save_path,task_type=TaskName.S21PEAK):

    if type(results)==dict:
        if "results" not in results.keys:
            results = results.get("results")
        elif "result" in results.keys():
            results = results.get("result")
    image = data
    dict_list = [np.array(image)]

    ply_plot_manager = QuantumPlotPlyManager()
    plt_plot_manager = QuantumPlotPltManager()
    print("plotting ai image...")
    print(save_path)
    fig_list = []

    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        save_path_png = str(save_path)
        save_path_html = save_path_png.replace("png","html")
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
def plot_s21(data,results,save_path):
    data = s21_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.S21PEAK)

    return fig_list

def plot_s21vsflux(data,results,save_path):
    data = s21vsflux_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.S21VFLUX)
    return fig_list
def plot_nns21vsflux(data,results,save_path):
    data = nns21vsflux_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=NNTaskName.S21VFLUX)
    return fig_list
def plot_drag(data,results,save_path):
    data = drag_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.DRAG)
    return fig_list

def plot_singleshot(data,results,save_path):
    data = singleshot_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.SINGLESHOT)
    return fig_list

def plot_nnspectrum2d(data,results,save_path):
    data = nnspectrum2d_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=NNTaskName.SPECTRUM2D)
    return fig_list

def plot_spectrum2d(data,results,save_path):
    data = spectrum2d_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.SPECTRUM2D)
    return fig_list

def plot_t1fit(data,results,save_path):
    data = t1fit_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.T1FIT)
    return fig_list

def plot_t2fit(data,results,save_path):
    data = t2fit_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.T2FIT)
    return fig_list

def plot_rabicos(data,results,save_path):
    data = rabicos_convert(data)
    fig_list = plot_template(data,results,save_path,task_type=TaskName.RABICOS)
    return fig_list