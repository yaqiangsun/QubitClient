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
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from resources.quark.anaylsis.utils import get_pkl_content
from resources.quark.anaylsis.inception import optpipulse,s21,s21vsflux,singleshot,nnspectrum2d,allxy_drag,nns21vsflux,spectrum2d
from resources.quark.anaylsis.visualization import plot_optpipulse,plot_s21,plot_s21vsflux,plot_singleshot,plot_nnspectrum2d,plot_drag,\
plot_nns21vsflux,plot_spectrum2d
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
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>=1:
                if task_key in "opt_pipulse":
                    analysis_result = optpipulse(data)
                    fig_list = plot_optpipulse(data,analysis_result,save_path='./tmp/vis/s21.png')
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
def main():
    task_key = "flux"
    base_dir = "tmp/data/s21vsflux"
    test_nns21vsflux(task_key,base_dir)

    # task_key = "spectrum"
    # base_dir = "tmp/data/nnspectrum2d"
    # test_nnspectrum2d(task_key,base_dir)
if __name__ == "__main__":
    main()