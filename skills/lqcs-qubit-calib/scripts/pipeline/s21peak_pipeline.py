# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/11
########################################################################


"""Real s21multi measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m skills.lqcs-qubit-calib.scripts.pipeline.s21peak_pipeline -q q1ld5 -b 0.0015 -n 200  -u True -c 0.6
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
import uuid
from datetime import datetime
from pathlib import Path
from PIL import Image
import json
import os

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import s21
from analysis.visualization import plot_s21
from analysis.update import s21_update

DEFAULT_SAVE_FOLDER = './tmp/db/result/image'


def parse_args():
    parser = argparse.ArgumentParser(description="S21 Multi Spectrum Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit name list, default: q1ld5")
    # 不填则从硬件查询
    parser.add_argument("--fread_star", "-f", type=float, default=None,
                        help="Manual readout fread_star (GHz). Auto query hardware if not set.")
    # 半带宽
    parser.add_argument("--bandwidth", "-b", type=float, default=0.001,
                        help="Frequency half bandwidth (GHz), default 0.005")
    # 采样点数
    parser.add_argument("--samples", "-n", type=int, default=200,
                        help="Number of frequency sampling points, default 200")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Folder to save spectrum plot image")
    
    # 是否根据分析结果更新参数
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update by analysis")
    
    # 置信度阈值，辅助决定是否根据分析结果更新参数
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="update by confidence threshold")
    

    return parser.parse_args()


# def llm_analysis(img_save_path):
    # resize更小
    # img_small_path = img_save_path.split('.png')[0] + '_small.png'
    # print("img_small_path: ", img_small_path)

    # with Image.open(img_save_path) as img:
        # w, h = img.size
        # new_w = w // 10
        # new_h = h // 10
        # print("size: ", new_w, new_h)
        # img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        # img_small.save(img_small_path, dpi=(300, 300))

    # test_qubit_spectroscopy_q1_describe(img_small_path)
    # test_qubit_spectroscopy_q2_classify(img_small_path)
    # test_qubit_spectroscopy_q3_reasoning(img_small_path)
    # test_qubit_spectroscopy_q4_assess(img_small_path)
    # test_qubit_spectroscopy_q5_extract(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    # print("\nQubit_Spectroscopy tests passed!")



def get_s21_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.S21.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    run_id = None
    qname = qubit_name_list[0]

    try:
        # =========== 查询/使用传入fread参数 ===========
        qubit_ctrl_client = QubitCtrlClient()
        
        if args.fread_star is not None:
            fread_star = args.fread_star
        else:
            fread_star = float(qubit_ctrl_client.query_param(qname=qname, key="fread_star"))

        # 设置实验参数
        set_params = {
            "qubits": qubit_name_list,
            "frequency_half_bandwidth": args.bandwidth,
            "frequency_sample_num": args.samples,
            "fread_star": fread_star
        }

        # 新建实验记录，写入存储
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[S21] Task started run_id={run_id[:8]}")
    
        # =========== 采集数据 ===========
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.S21,
            qubits=qubit_name_list,
            frequency_center=set_params["fread_star"],
            frequency_half_bandwidth=set_params["frequency_half_bandwidth"],
            frequency_sample_num=set_params["frequency_sample_num"]
        )

        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # =========== 写入原始数据 ===========
        store.update_run(run_id=run_id, raw_data_id=data_id, raw_data=raw_data)

        # =========== 分析 ============
        analysis_result = s21(raw_data)

        # =========== 绘制波形图==========
        img_save_path = f'{save_folder}/{CtrlTaskName.S21.value}_{qubit_name_list[0]}_{run_id}.png'
 
        plot_s21(raw_data, analysis_result, save_path=img_save_path)

        img_save_path = os.path.abspath(img_save_path)
        plot_paths = [img_save_path]

        # =========== 接入大模型分析图片 ===========
        # llm_analysis(img_save_path)

        # =========== 自动更新参数 ==============
        new_full_params = set_params.copy()
        if args.update:

            update_dict = s21_update(results=analysis_result, conf_threshold=args.confidence, qubit_name_list=qubit_name_list)
            
            for qname, info in update_dict.items():
                new_value = info["fread_star"]

                qubit_ctrl_client.update_param(
                    qname=qname,
                    task_type=CtrlTaskName.S21,
                    values=[new_value]
                )
                # 覆盖新频率到参数字典
                new_full_params["fread_star"] = float(new_value)

        # =========== 更新结果到存储 ======================
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        print(f"测量完成，更新： {new_full_params}")

    except Exception as e:
        err_msg = f"测量异常：{str(e)}"
        if run_id is not None:
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
    get_s21_hdf5_res(cli_args)