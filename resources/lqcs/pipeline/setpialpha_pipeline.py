# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/17
########################################################################


"""SETPIALPHA measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: python -m tests.ui.serve
    2. cmd params example:
            python -m resources.lqcs.pipeline.setpialpha_pipeline -q q3lu7 -ms 1,4,8 -g X -s ./tmp
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
import json
import numpy as np

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import setpialpha
from analysis.visualization import plot_setpialpha

SAVE_PLOT_FOLDER = './tmp'

qubit_ctrl_client = QubitCtrlClient()


def parse_args():
    parser = argparse.ArgumentParser(description="SETPIALPHA Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit name list, default: q3lu7")
    # ms序列，逗号分隔
    parser.add_argument("--ms", "-ms", type=str, default="1,4,8",
                        help="ms list for SETPIALPHA, split by comma, default '1,4,8'")
    # gate类型
    parser.add_argument("--gate", "-g", type=str, default="X",
                        help="Gate type, default X")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save plot image")
    return parser.parse_args()


def get_construct_data(q_name, lines_color, filepath_1, filepath_2, filepath_3):
    if 'blue' in lines_color:
        pos = 1
    else: # orange
        pos = 2
    piamp_file_1 = filepath_1
    piamp_data_1 = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=piamp_file_1)
    piamp_data_1 = json.loads(piamp_data_1[0]["text"])
    data = piamp_data_1[q_name]
    data_arr = np.array(data)
    x_1 = data_arr[:, 0]
    col_blue_1 = data_arr[:, pos]  # 1: blue, 2: orange

    piamp_file_2 = filepath_2
    piamp_data_2 = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=piamp_file_2)
    piamp_data_2 = json.loads(piamp_data_2[0]["text"])
    data = piamp_data_2[q_name]
    data_arr = np.array(data)
    col_blue_2 = data_arr[:, pos]  # 1: blue, 2: orange

    piamp_file_3 = filepath_3
    piamp_data_3 = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=piamp_file_3)
    piamp_data_3 = json.loads(piamp_data_3[0]["text"])
    data = piamp_data_3[q_name]
    data_arr = np.array(data)
    col_blue_3 = data_arr[:, pos]  # 1: blue, 2: orange

    # {'q1lu7': [[..]]}
    waves = np.array([col_blue_1, col_blue_2, col_blue_3]) # (3, 11)
    construct_data = {q_name: [waves, np.array(x_1), 0.1, 0.1]}
    return construct_data


def get_setpialpha_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "setpialpha"
    pipeline_type = "setpialpha_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    q_name = qubit_name_list[0]
    ms_list = [int(x.strip()) for x in args.ms.split(",")]
    gate_val = args.gate

    try:
        # 组装实验基础参数
        set_params = {
            "qubits": qubit_name_list,
            "ms": ms_list,
            "gate": gate_val
        }

        # 新建实验记录，写入存储
        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[SETPIALPHA] Task started run_id={run_id[:8]}")

        # 1.采集数据 - X门
        data = qubit_ctrl_client.run(CtrlTaskName.SETPIALPHA,
                                       qubits=qubit_name_list,
                                       ms=ms_list,
                                       gate=gate_val)
        data_id = data[0]["text"]
        data_id = json.loads(data_id)
        # 得到6个文件名
        print("data_id: ", data_id)

        store.update_run(
            run_id=run_id,
            raw_data_id=data_id[0][0]
        )
        # 先不存raw-data有六个

        plot_paths = []
        last_analysis_result = None

        # three piamp files' blue lines
        construct_data = get_construct_data(q_name, 'blue', data_id[0][0], data_id[0][1], data_id[0][2])
        # 2.分析数据
        analysis_result = setpialpha(construct_data)
        last_analysis_result = analysis_result
        # 3.绘图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/setpialpha_piamp_bluelines_{pure_name}.png'
        fig_list = plot_setpialpha(construct_data, analysis_result, save_path=img_save_path)
        plot_paths.append(img_save_path)

        # three piamp files' orange lines
        construct_data = get_construct_data(q_name, 'orange', data_id[0][0], data_id[0][1], data_id[0][2])
        # 2.分析数据
        analysis_result = setpialpha(construct_data)
        last_analysis_result = analysis_result
        # 3.绘图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/setpialpha_piamp_orangelines_{pure_name}.png'
        fig_list = plot_setpialpha(construct_data, analysis_result, save_path=img_save_path)
        plot_paths.append(img_save_path)

        # three alpha files' blue lines
        construct_data = get_construct_data(q_name, 'blue', data_id[1][0], data_id[1][1], data_id[1][2])
        # 2.分析数据
        analysis_result = setpialpha(construct_data)
        last_analysis_result = analysis_result
        # 3.绘图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/setpialpha_alpha_bluelines_{pure_name}.png'
        fig_list = plot_setpialpha(construct_data, analysis_result, save_path=img_save_path)
        plot_paths.append(img_save_path)

        # three alpha files' orange lines
        construct_data = get_construct_data(q_name, 'orange', data_id[1][0], data_id[1][1], data_id[1][2])
        # 2.分析数据
        analysis_result = setpialpha(construct_data)
        last_analysis_result = analysis_result
        # 3.绘图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/setpialpha_alpha_orangelines_{pure_name}.png'
        fig_list = plot_setpialpha(construct_data, analysis_result, save_path=img_save_path)
        plot_paths.append(img_save_path)

        # 4.接入大模型分析图片
        # resize更小
        # img_small_path = img_save_path.split('.png')[0] + '_small.png'
        # print("img_small_path: ", img_small_path)

        # with Image.open(img_save_path) as img:
        #     w, h = img.size
        #     new_w = w // 10
        #     new_h = h // 10
        #     print("size: ", new_w, new_h)
        #     img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        #     img_small.save(img_small_path, dpi=(300, 300))

        # test_qubit_spectroscopy_q1_describe(img_small_path)
        # test_qubit_spectroscopy_q2_classify(img_small_path)
        # test_qubit_spectroscopy_q3_reasoning(img_small_path)
        # test_qubit_spectroscopy_q4_assess(img_small_path)
        # test_qubit_spectroscopy_q5_describe(img_small_path)
        # test_qubit_spectroscopy_q6_status(img_small_path)
        # print("\nQubit_Spectroscopy tests passed!")

        # 5.更新PiGate.amp和PiGate.alpha
        if type(last_analysis_result)==dict:
                if "results" not in last_analysis_result.keys():
                    last_analysis_result = last_analysis_result.get("results")
                elif "result" in last_analysis_result.keys():
                    last_analysis_result = last_analysis_result.get("result")
        for result in last_analysis_result:
            params_list = result['params']
            confs_list = result['confs']

            params_list = result.get("params", [])
            confs_list  = result.get("confs", [])
            for i in range(len(qubit_name_list)):
                peaks = params_list[i]
                confs = confs_list[i]
                if len(confs) > 0:
                    best_idx = confs.index(max(confs))
                    best_peak = peaks[best_idx]
                    target_amp =best_peak
                    target_alpha="Null"
                    values=str(target_amp) + ',' + target_alpha
                    qname=qubit_name_list[i]
                    task_type=CtrlTaskName.SETPIALPHA
                    print("更新values-----------", values)
                    qubit_ctrl_client.update_param(qname=qname, task_type=task_type, values=values)

        # 6.更新PiHalf.amp和PiHalf.alpha
       
        # qname=qubit_name_list[0]
        # task_type=CtrlTaskName.SETPIALPHA
        # values="Null,Null,3.193120459017055,3.193120459017055"   
        # qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

        new_full_params = set_params.copy()
        # new_full_params["all_plot_paths"] = plot_paths 不需要记录

        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=last_analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        print(f"SETPIALPHA测量完成，基础参数：{set_params}")

    except Exception as e:
        err_msg = f"SETPIALPHA测量异常：{str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        print(f"任务失败 run_id={run_id[:8]} 错误：{err_msg}")
        raise


if __name__ == '__main__':
    cli_args = parse_args()
    get_setpialpha_hdf5_res(cli_args)