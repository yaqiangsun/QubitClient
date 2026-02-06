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
from .wrapper_handler import handle_exceptions, control_api_execution

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
        results = results.get("results")
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
def nnplot_spectrum2d(report,basepath,name):
    save_path = get_path(report,basepath,name)
    results = report.analysis
    other_infomation = report.other_infomation

    results = results
    data_ndarray = other_infomation
    path = save_path

    nums = len(results)
    row = (nums // 3) + 1 if nums % 3 != 0 else nums // 3
    col = min(nums, 3)

    fig = plt.figure(figsize=(5 * col, 4 * row))
    data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
    data_dict = data_dict['image']
    dict_list = []
    q_list = data_dict.keys()

    for idx, q_name in enumerate(q_list):
        npz_dict = {}
        image_q = data_dict[q_name]
        data = image_q[0]
        if data.ndim != 2:
            raise ValueError("数据格式无效，data不是二维数组")
        data = np.array(data)
        data = np.abs(data)
        npz_dict['bias'] = image_q[1]
        npz_dict['frequency'] = image_q[2]
        npz_dict['iq_avg'] = data
        npz_dict['name'] = q_name
        dict_list.append(npz_dict)

    for index in range(nums):
        ax = fig.add_subplot(row, col, index + 1)
        result = results[index]

        points_list = []
        for i in range(len(result["linepoints_list"])):
            points_list.append(result["linepoints_list"][i])

        plt.pcolormesh(dict_list[index]["bias"], dict_list[index]["frequency"],  dict_list[index]["iq_avg"], shading='auto', cmap='viridis')
        plt.colorbar(label='IQ Average')  # 添加颜色条
        colors = plt.cm.rainbow(np.linspace(0, 1, len(result["linepoints_list"])))
        for i in range(len(points_list)):
            reflection_points = points_list[i]
            reflection_points = np.array(reflection_points)
            xy_x = reflection_points[:, 0]  # 提取 x 坐标
            xy_y = reflection_points[:, 1]  # 提取 y 坐标
            plt.scatter(xy_x, xy_y, color=colors[i], label=f'XY Points{i}-conf:{round(result["confidence_list"][i],2)}', s=5, alpha=0.1)  # 绘制散点图
        # 图形设置
        file_name = dict_list[index]["name"]
        plt.title(f"File: {file_name}")

        plt.xlabel("Bias")
        plt.ylabel("Frequency (GHz)")
        plt.legend()
    fig.tight_layout()
    save_path = path
    fig.savefig(save_path)
    logging.info(f"Saving ai image to:{save_path}")
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