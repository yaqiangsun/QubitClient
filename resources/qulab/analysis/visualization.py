# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/01/27 18:04:52
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

def get_path(report,basepath,name):


    results = report.analysis
    other_infomation = report.other_infomation
    image = other_infomation['image']
    ID = other_infomation.get('id')

    fold=None
    today=date.today()
    basepath_ai = Path(basepath) if fold is None else Path(basepath+f'/{fold}')
    basepath_ai = basepath_ai/today.strftime('%Y%m%d')
    foder=os.path.exists(basepath_ai)
    print(basepath_ai)
    if foder:
        filenames = np.load(basepath_ai/r'filenames.npz',allow_pickle=True)['filenames'].tolist()
        # print('Exist!')
    else:
        os.makedirs(basepath_ai)
        filenames = {}
        print('New folder!')
    
    title = ''.join((name, '_', *image.keys(), '_id=', str(ID), 'index',
                     str(report.index)))
    a = filenames[title]  if title in filenames else 0
    title_new = title+f'_{a}'
    title_new_fig = title_new + 'ai.png'
    png_path = basepath_ai / title_new_fig
    return png_path
def plot_template(report,basepath,name,task_type=TaskName.S21PEAK):
    save_path = get_path(report,basepath,name)
    results = report.analysis
    other_infomation = report.other_infomation


    if type(results)==dict:
        if "results" not in results.keys:
            results = results.get("results")
        elif "result" in results.keys():
            results = results.get("result")
    image = other_infomation
    # image = np.array(other_infomation)
    dict_list = [np.array(image)]

    ply_plot_manager = QuantumPlotPlyManager()
    plt_plot_manager = QuantumPlotPltManager()
    print("plotting ai image...")
    print(save_path)

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
        fig_ply = ply_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=task_type.value,
            save_path=save_path_html,
            result=result,
            dict_param=dict_param
        )
    logging.info(f"Saving ai image to:{save_path}")


####################################################################################
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_nnspectrum2d(data,results,save_path):
    fig_list = plot_template(data,results,save_path,task_type=NNTaskName.SPECTRUM2D)
    return fig_list
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnplot_powershift(report,basepath,name):
    plot_template(report,basepath,name,NNTaskName.POWERSHIFT)
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnplot_spectrum(report,basepath,name):
    plot_template(report,basepath,name,NNTaskName.SPECTRUM)

####################################################################################
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_s21(report,basepath,name):
    plot_template(report,basepath,name,TaskName.S21PEAK)
    
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_rabi(report, basepath, name):
    other_infomation, _= report.other_infomation
    report.other_infomation = other_infomation
    plot_template(report,basepath,name,TaskName.RABICOS)

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_ramsey(report, basepath, name):
    other_infomation, _, _, _, _= report.other_infomation
    report.other_infomation = other_infomation
    plot_template(report,basepath,name,TaskName.RAMSEY)

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_t1fit(report, basepath, name):
    plot_template(report,basepath,name,TaskName.T1FIT)
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_t2fit(report, basepath, name):
    plot_template(report,basepath,name,TaskName.T2FIT)

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_optpipulse(report, basepath, name):
    other_infomation, _= report.other_infomation
    report.other_infomation = other_infomation
    plot_template(report,basepath,name,TaskName.OPTPIPULSE)

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_spectrum(report,basepath,name):
    plot_template(report,basepath,name,TaskName.SPECTRUM)

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_powershift(report,basepath,name):
    plot_template(report,basepath,name,TaskName.POWERSHIFT)


@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_s21vsflux(report,basepath,name):
    plot_template(report,basepath,name,TaskName.S21VFLUX)


@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_allxy_drag(report,basepath,name):
    plot_template(report,basepath,name,TaskName.DRAG)

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def plot_singleshot(report,basepath,name):
    other_infomation, _= report.other_infomation
    report.other_infomation = other_infomation
    plot_template(report,basepath,name,TaskName.SINGLESHOT)