# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################


"""S21 vs Flux 2D scan pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m skills.lqcs-qubit-calib.scripts.pipeline.s21vsflux_pipeline -q q1ld5 -b 0.001 -n 11 -u True -c 0.4
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
from PIL import Image
import os
import numpy as np

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import s21vsflux
from analysis.visualization import plot_s21vsflux

DEFAULT_SAVE_FOLDER = './tmp/db/result/image'


def parse_args():
    parser = argparse.ArgumentParser(description="S21VSFLUX 2D Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit name list, default: q1ld5")
    # 手动指定读取频率
    parser.add_argument("--fread", "-f", type=float, default=None,
                        help="Manual readout freq(GHz), auto query hardware if empty")
    # 频率半带宽
    parser.add_argument("--bandwidth", "-b", type=float, default=0.03,
                        help="Freq half bandwidth(GHz), default 0.001")
    # 频率采样点数
    parser.add_argument("--samples", "-n", type=int, default=11,
                        help="Freq sample count, default 11")
    # 偏置起始值
    parser.add_argument("--bias-start", type=float, default=-3, help="Flux bias start")
    # 偏置终止值
    parser.add_argument("--bias-end", type=float, default=3, help="Flux bias end")
    # 偏置采样点数
    parser.add_argument("--bias-samples", type=int, default=16, help="Bias sample count")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    # 是否根据分析结果更新参数
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    # 置信度阈值
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
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



def get_s21vsflux_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.S21VSFLUX.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    qname = qubit_name_list[0]

    try:
        qubit_ctrl_client = QubitCtrlClient()
        
        task_type = CtrlTaskName.S21VSFLUX

        # 获取读取腔频率
        if args.fread is not None:
            fread = args.fread
        else:
            fread_ret = qubit_ctrl_client.query_param(qname=qname, key="fread_star")
            fread = float(fread_ret)

        # 组装实验参数
        set_params = {
            "qubits": qubit_name_list,
            "frequency_half_bandwidth": args.bandwidth,
            "frequency_sample_num": args.samples,
            "frequency_center": fread,
            "read_bias_start": args.bias_start,
            "read_bias_end": args.bias_end,
            "read_bias_sample_num": args.bias_samples
        }

        # 创建实验记录，移除 pipeline_type
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[S21VSFLUX] Task started run_id={run_id[:8]}")

        # 硬件采集数据
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.S21VSFLUX,
            qubits=qubit_name_list,
            freq_center=fread,
            freq_half_bandwidth=args.bandwidth,
            freq_sample_num=args.samples,
            read_bias_start=args.bias_start,
            read_bias_end=args.bias_end,
            read_bias_sample_num=args.bias_samples
        )

        # 读取原始数据
        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 写入原始数据到存储
        store.update_run(run_id=run_id, raw_data_id=data_id, raw_data=raw_data)

        # 数据分析
        analysis_result = s21vsflux(raw_data)

        # 绘制图像
        img_save_path = f'{save_folder}/{CtrlTaskName.S21VSFLUX.value}_{qname}_{run_id}.png'
        plot_s21vsflux(raw_data, analysis_result, save_path=img_save_path)

        img_save_path = os.path.abspath(img_save_path)
        plot_paths = [img_save_path]

        # =========== 接入大模型分析图片 ===========
        # llm_analysis(img_save_path)

        new_full_params = set_params.copy()
        update_map = {}

        # 不更新参数

        # 任务完成，更新全量结果至存储
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        logging.info(f"测量完成，最终参数： {new_full_params}")

    except Exception as e:
        err_msg = f"测量异常：{str(e)}"
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
    get_s21vsflux_hdf5_res(cli_args)