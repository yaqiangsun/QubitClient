# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 11:48:16
########################################################################



import os
import sys
import logging
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from resources.quark.anaylsis.utils import get_pkl_content
from resources.quark.anaylsis.inception import optpipulse,s21,s21vsflux,singleshot,\
                                                nnspectrum2d,allxy_drag,nns21vsflux,\
                                                spectrum2d,t1fit,t2fit,rabicos,nnspectrum
from resources.quark.anaylsis.visualization import plot_optpipulse,plot_s21,\
                                                    plot_s21vsflux,plot_singleshot,plot_nnspectrum2d,plot_drag,\
                                                    plot_nns21vsflux,plot_spectrum2d,plot_t1fit,\
                                                    plot_t2fit,plot_rabicos,plot_nnspectrum
import matplotlib.pyplot as plt




def test_optpipulse(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if "opt" in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "opt_pipulse":
                    analysis_result = optpipulse(data)
                    fig_list = plot_optpipulse(data,analysis_result,save_path='./tmp/vis/optpipulse.png')
                    fig_list[0].show()
                    plt.show(block=True)


def test_s21peak(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "s21peak":
                    analysis_result = s21(data)
                    fig_list = plot_s21(data,analysis_result,save_path='./tmp/vis/s21.png')
                    fig_list[0].show()
                    plt.show(block=True)
def test_s21vsflux(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "s21vflux":
                    analysis_result = s21vsflux(data)
                    fig_list = plot_s21vsflux(data,analysis_result,save_path='./tmp/vis/s21vsflux.png')
                    fig_list[0].show()
                    plt.show(block=True)
def test_nns21vsflux(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "nns21vsflux":
                    analysis_result = nns21vsflux(data)
                    fig_list = plot_nns21vsflux(data,analysis_result,save_path='./tmp/vis/nns21vsflux.png')
                    fig_list[0].show()
                    plt.show(block=True)
def test_singleshot(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "singleshot":
                    analysis_result = singleshot(data)
                    fig_list = plot_singleshot(data,analysis_result,save_path='./tmp/vis/singleshot.png')
                    fig_list[0].show()
                    plt.show(block=True)
def test_nnspectrum2d(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "nnspectrum2d":
                    analysis_result = nnspectrum2d(data)
                    fig_list = plot_nnspectrum2d(data,analysis_result,save_path='./tmp/vis/nnspectrum2d.png')
                    fig_list[0].show()
                    plt.show(block=True)
def test_spectrum2d(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "spectrum2d":
                    analysis_result = spectrum2d(data)
                    fig_list = plot_spectrum2d(data,analysis_result,save_path='./tmp/vis/spectrum2d.png')
                    fig_list[0].show()
                    plt.show(block=True)
def test_drag(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "drag":
                    analysis_result = allxy_drag(data)
                    fig_list = plot_drag(data,analysis_result,save_path='./tmp/vis/drag.png')
                    fig_list[0].show()
                    plt.show(block=True)


def test_rabicos(task_key, base_dir):
    found_files = 0
    for filename in os.listdir(base_dir):
        if not filename.endswith('.pkl'):
            continue
        pkl_path = os.path.join(base_dir, filename)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data or "name" not in data["meta"]:
            continue
        name_lower = data["meta"]["name"].lower()
        if "rabi" in name_lower:
            qubits = data["meta"]["other"].get("qubits", [])
            if len(qubits) >= 1:
                found_files += 1
                print(f"正在测试 Rabi 文件 ({found_files}): {pkl_path}")
  
                analysis_result = rabicos(data)
                fig_list = plot_rabicos(data, analysis_result, save_path='./tmp/vis/rabicos.png')
                if fig_list and len(fig_list) > 0:
                    fig_list[0].show()
                plt.show(block=True)


def test_t1fit(task_key, base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if "t1" in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"]) >= 1:
                if task_key in ["t1fit", "t1"]:
                    print(f"正在测试 t1fit 文件: {pkl_path}")
                    analysis_result = t1fit(data)
                    #print("第一个 qubit 的 results 示例：", analysis_result.get("results", [{}])[0])                                        
                    fig_list = plot_t1fit(data, analysis_result, save_path='./tmp/vis/t1fit.png')
                    if fig_list and len(fig_list) > 0:
                        fig_list[0].show()
                    plt.show(block=True)


def test_t2fit(task_key, base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if "t2" or "ramsey" in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"]) >= 1:
                if task_key in ["t2fit", "t2", "ramsey", "echo"]:
                    print(f"正在测试 t2fit 文件: {pkl_path}")
                    analysis_result = t2fit(data)
                    # print("分析完成，结果示例：", analysis_result.get("results", [{}])[0])
                    fig_list = plot_t2fit(data, analysis_result, save_path='./tmp/vis/t2fit.png')
                    if fig_list and len(fig_list) > 0:
                        fig_list[0].show()
                    plt.show(block=True)

def test_nnspectrum(task_key,base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        print(f" print task_key: {task_key}, data name: {data['meta']['name']}")

        # 因为是拿spectrum数据来测nnscope所以False
        # if task_key.lower() in data["meta"]["name"].lower():
        if "spectrum" in data["meta"]["name"].lower():
            if len(data["meta"]["other"].get("qubits",[]))>=1:
                logging.info("task_key: %s, qubits: %s", task_key, data["meta"]["other"]["qubits"])
                if task_key in "spectrum":
                    analysis_result = nnspectrum(data)
                    logging.info(f"-----nnspectrum analysis result: {analysis_result}")
                    fig_list = plot_nnspectrum(data,analysis_result,save_path='./tmp/vis/nnspectrum.png')
                    fig_list[0].show()
                    plt.show(block=True)

def main():
    # task_key = "flux"
    # base_dir = "tmp/data/s21vsflux"
    # test_nns21vsflux(task_key,base_dir)

    # task_key = "s21"
    # base_dir = "tmp/s21"
    # test_s21peak(task_key,base_dir)
    task_key = "spectrum"
    base_dir = "tmp/data/spectrum"
    test_nnspectrum(task_key,base_dir)

    # task_key = "spectrum"
    # base_dir = "tmp/data/nnspectrum2d"
    # test_nnspectrum2d(task_key,base_dir)

    # task_key = "rabi"
    # base_dir = "data/rabi_in_group_q"
    # test_rabicos(task_key,base_dir)
    # task_key = "t1"
    # base_dir = "data/t1_data_q"
    # test_t1fit(task_key,base_dir)
    # task_key = "t2"
    # base_dir = "data/t2_data_q"
    # test_t2fit(task_key,base_dir)
    # task_key = "opt"
    # base_dir = "data/opt_pipulse_q"
    # test_optpipulse(task_key,base_dir)

if __name__ == "__main__":
    main()