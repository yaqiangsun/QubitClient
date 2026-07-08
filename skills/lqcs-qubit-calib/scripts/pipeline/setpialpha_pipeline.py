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
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m skills.lqcs-qubit-calib.scripts.pipeline.setpialpha_pipeline -q q1ld5  -g X -u True -c 0.1
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
import os
import numpy as np
import logging

# 统一日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import setpialpha
from analysis.visualization import plot_setpialpha
from analysis.update import setpialpha_update

SAVE_PLOT_FOLDER ='./tmp/db/result/image'

qubit_ctrl_client = QubitCtrlClient()


def llm_analysis(img_save_path):
    # resize更小
    img_small_path = img_save_path.split('.png')[0] + '_small.png'
    logging.info(f"img_small_path: {img_small_path}")

    with Image.open(img_save_path) as img:
        w, h = img.size
        new_w = w // 10
        new_h = h // 10
        logging.info(f"size: {new_w}, {new_h}")
        img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img_small.save(img_small_path, dpi=(300, 300))

    # test_qubit_spectroscopy_q1_describe(img_small_path)
    # test_qubit_spectroscopy_q2_classify(img_small_path)
    # test_qubit_spectroscopy_q3_reasoning(img_small_path)
    # test_qubit_spectroscopy_q4_assess(img_small_path)
    # test_qubit_spectroscopy_q5_describe(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    logging.info("Qubit_Spectroscopy tests passed!")


def parse_args():
    parser = argparse.ArgumentParser(description="SETPIALPHA Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit name list, default: q1ld5")
    # pipulse_num，逗号分隔
    parser.add_argument("--pipulse_num", "-n", type=str, default="1,4,8",
                        help="pipulse_num for SETPIALPHA, split by comma, default '1,4,8'")
    # gate类型
    parser.add_argument("--gate", "-g", type=str, default="X",
                        help="Gate type, default X")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save plot image")
    # 新增更新开关、置信度阈值
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_construct_data(q_name, lines_color, filepath_1, filepath_2, filepath_3):
    if 'blue' in lines_color:
        pos = 1
    else:  # orange
        pos = 2
    piamp_file_1 = filepath_1
    piamp_data_1 = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=piamp_file_1)
    data = piamp_data_1[q_name]
    data_arr = np.array(data)
    x_1 = data_arr[:, 0]
    col_blue_1 = data_arr[:, pos]  # 1: blue, 2: orange

    piamp_file_2 = filepath_2
    piamp_data_2 = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=piamp_file_2)
    data = piamp_data_2[q_name]
    data_arr = np.array(data)
    col_blue_2 = data_arr[:, pos]  # 1: blue, 2: orange

    piamp_file_3 = filepath_3
    piamp_data_3 = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=piamp_file_3)
    data = piamp_data_3[q_name]
    data_arr = np.array(data)
    col_blue_3 = data_arr[:, pos]  # 1: blue, 2: orange

    waves = np.array([col_blue_1, col_blue_2, col_blue_3])  # (3, 11)
    construct_data = {q_name: [waves, np.array(x_1), 0.1, 0.1]}
    return construct_data


def get_setpialpha_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_type = CtrlTaskName.SETPIALPHA
    task_name = CtrlTaskName.SETPIALPHA.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    q_name = qubit_name_list[0]
    pipulse_num = [int(x.strip()) for x in args.pipulse_num.split(",")]
    gate_val = args.gate

    try:
        # 组装实验基础参数
        set_params = {
            "qubits": qubit_name_list,
            "pipulse_num": pipulse_num,
            "gate": gate_val
        }

        # 新建实验记录，移除 pipeline_type
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[SETPIALPHA] Task started run_id={run_id[:8]}")

        # 1.采集数据
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.SETPIALPHA,
            qubits=qubit_name_list,
            pipulse_num=pipulse_num,
            gate=gate_val
        )

        logging.info("data_id: %s", data_id)

        store.update_run(
            run_id=run_id,
            raw_data_id=data_id[0][0]
        )

        plot_paths = []
        last_analysis_result = None

        # three piamp files' blue lines
        construct_data = get_construct_data(q_name, 'blue', data_id[0][0], data_id[0][1], data_id[0][2])
        analysis_result = setpialpha(construct_data)
        last_analysis_result = analysis_result
        img_save_path = f'{save_folder}/{CtrlTaskName.SETPIALPHA}_piamp_bluelines_{q_name}_{run_id}.png'
        plot_setpialpha(construct_data, analysis_result, save_path=img_save_path)
        img_save_path = os.path.abspath(img_save_path)
        plot_paths.append(img_save_path)

        # three piamp files' orange lines
        construct_data = get_construct_data(q_name, 'orange', data_id[0][0], data_id[0][1], data_id[0][2])
        analysis_result = setpialpha(construct_data)
        last_analysis_result = analysis_result
        img_save_path = f'{save_folder}/{CtrlTaskName.SETPIALPHA}_piamp_orangelines_{q_name}_{run_id}.png'
        plot_setpialpha(construct_data, analysis_result, save_path=img_save_path)
        img_save_path = os.path.abspath(img_save_path)
        plot_paths.append(img_save_path)

        # three alpha files' blue lines
        construct_data = get_construct_data(q_name, 'blue', data_id[1][0], data_id[1][1], data_id[1][2])
        analysis_result = setpialpha(construct_data)
        last_analysis_result = analysis_result
        img_save_path = f'{save_folder}/{CtrlTaskName.SETPIALPHA}_alpha_bluelines_{q_name}_{run_id}.png'
        plot_setpialpha(construct_data, analysis_result, save_path=img_save_path)
        img_save_path = os.path.abspath(img_save_path)
        plot_paths.append(img_save_path)

        # three alpha files' orange lines
        construct_data = get_construct_data(q_name, 'orange', data_id[1][0], data_id[1][1], data_id[1][2])
        analysis_result = setpialpha(construct_data)
        last_analysis_result = analysis_result
        img_save_path = f'{save_folder}/{CtrlTaskName.SETPIALPHA}_alpha_orangelines_{q_name}_{run_id}.png'
        plot_setpialpha(construct_data, analysis_result, save_path=img_save_path)
        img_save_path = os.path.abspath(img_save_path)
        plot_paths.append(img_save_path)

        # 开启参数更新
        if args.update:
            update_map = setpialpha_update(
                results=last_analysis_result,
                conf_threshold=args.confidence,
                qubit_name_list=qubit_name_list
            )
            # 下发参数
            for qname, val_list in update_map.items():
                qubit_ctrl_client.update_param(qname=qname, task_type=task_type, values=val_list)
                logging.info("update values: %s", val_list)

        new_full_params = set_params.copy()

        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=last_analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        logging.info(f"SETPIALPHA测量完成，基础参数：{set_params}")

    except Exception as e:
        err_msg = f"SETPIALPHA测量异常：{str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        logging.error(f"任务失败 run_id={run_id[:8]} 错误：{err_msg}")
        raise


if __name__ == '__main__':
    cli_args = parse_args()
    get_setpialpha_hdf5_res(cli_args)