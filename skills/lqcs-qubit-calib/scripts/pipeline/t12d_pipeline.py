# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/15
########################################################################


"""T1 2D measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example: (-dn must be bigger than 10)
            python -m resources.lqcs.pipeline.t12d_pipeline -q q3lu7 -bs -1.0 -be 0.4 -bn 20 -ds 0 -de 50000 -dn 13 -s ./tmp
"""

import sys
import argparse
import math
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

from analysis.inception import t12dfit
from analysis.visualization import plot_t12dfit

SAVE_PLOT_FOLDER = './tmp'


def parse_args():
    parser = argparse.ArgumentParser(description="T1 2D Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit name list, default: q3lu7")
    # 偏置起始
    parser.add_argument("--zpa-start", "-bs", type=float, default=-1.0,
                        help="zpa start value, default -1.0")
    # 偏置终止
    parser.add_argument("--zpa-end", "-be", type=float, default=0.4,
                        help="zpa end value, default 0.4")
    # 偏置采样点数
    parser.add_argument("--zpa-sample-num", "-bn", type=int, default=71,
                        help="zpa sampling count, default 71")
    # 延时起始
    parser.add_argument("--delay-start", "-ds", type=int, default=0,
                        help="Delay start value, default 0")
    # 延时终止
    parser.add_argument("--delay-end", "-de", type=int, default=80000,
                        help="Delay end value, default 80000")
    # 延时采样点数
    parser.add_argument("--delay-sample-num", "-dn", type=int, default=17,
                        help="Delay sampling count, default 17")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save spectrum plot image")
    return parser.parse_args()


def get_t12d_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "t1_2d"
    pipeline_type = "t1_2d_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 设置实验参数
        set_params = {
            "qubits": qubit_name_list,
            "zpa_start": args.zpa_start,
            "zpa_end": args.zpa_end,
            "zpa_sample_num": args.zpa_sample_num,
            "delay_start": args.delay_start,
            "delay_end": args.delay_end,
            "delay_sample_num": args.delay_sample_num
        }

        # 新建实验记录，写入存储
        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[T1_2D] Task started run_id={run_id[:8]}")
    
        # =========== 采集数据 ===========
        data = qubit_ctrl_client.run(
            CtrlTaskName.T1_2D,
            qubits=qubit_name_list,
            zpa_start=set_params["zpa_start"],
            zpa_end=set_params["zpa_end"],
            zpa_sample_num=set_params["zpa_sample_num"],
            delay_start=set_params["delay_start"],
            delay_end=set_params["delay_end"],
            delay_sample_num=set_params["delay_sample_num"]
        )
        data_id = data[0]["text"]
        raw_data_text = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
        raw_data = json.loads(raw_data_text[0]["text"])

        # =========== 写入原始数据 ===========
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # =========== 分析 ============
        analysis_result = t12dfit(raw_data)

        print("analysis: ", analysis_result)

        # =========== 绘制波形图==========
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/t1_2d_{pure_name}.png'
        fig_list = plot_t12dfit(raw_data, analysis_result, save_path=img_save_path)
        plot_paths = [img_save_path]

        # =========== 接入大模型分析图片 ===========
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
        # test_qubit_spectroscopy_q5_extract(img_small_path)
        # test_qubit_spectroscopy_q6_status(img_small_path)
        # print("\nQubit_Spectroscopy tests passed!")

        # =========== 无参数更新，沿用原参数 ==============
        new_full_params = set_params.copy()

        # =========== 更新结果到存储 ======================
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        print(f"测量完成，参数： {new_full_params}")

    except Exception as e:
        # ========== 捕获异常，存入错误信息 ================
        err_msg = f"T1二维测量异常：{str(e)}"
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
    get_t12d_hdf5_res(cli_args)