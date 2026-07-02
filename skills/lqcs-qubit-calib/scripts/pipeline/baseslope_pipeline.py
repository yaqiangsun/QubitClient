# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/16
########################################################################


"""Baseslope measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m skills.lqcs-qubit-calib.scripts.pipeline.baseslope_pipeline -q Q0 Q1 -ds 1.0 -de 100.0 -dn 50 -sh 0 -s ./tmp
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
from PIL import Image
import json

# 统一日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import baseslope
from analysis.visualization import plot_baseslope

DEFAULT_SAVE_FOLDER = './tmp'


def llm_analysis(img_save_path):
    # resize更小
    img_small_path = img_save_path.split('.png')[0] + '_small.png'
    print("img_small_path: ", img_small_path)

    with Image.open(img_save_path) as img:
        w, h = img.size
        new_w = w // 10
        new_h = h // 10
        print("size: ", new_w, new_h)
        img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img_small.save(img_small_path, dpi=(300, 300))

    # test_qubit_spectroscopy_q1_describe(img_small_path)
    # test_qubit_spectroscopy_q2_classify(img_small_path)
    # test_qubit_spectroscopy_q3_reasoning(img_small_path)
    # test_qubit_spectroscopy_q4_assess(img_small_path)
    # test_qubit_spectroscopy_q5_extract(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    print("\nQubit_Spectroscopy tests passed!")


def parse_args():
    parser = argparse.ArgumentParser(description="Baseslope Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["Q0", "Q1"],
                        help="Target qubit name list, default: Q0 Q1")
    # 延时起始值
    parser.add_argument("--delay-start", "-ds", type=float, default=1.0,
                        help="Delay start value")
    # 延时终止值
    parser.add_argument("--delay-end", "-de", type=float, default=100.0,
                        help="Delay end value")
    # 延时采样点数
    parser.add_argument("--delay-sample-num", "-dn", type=float, default=50,
                        help="Delay sample number")
    # 阶跃高度
    parser.add_argument("--step-height", "-sh", type=float, default=0,
                        help="Step height value")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Folder to save plot image")

    return parser.parse_args()


def get_baseslope_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.BASESLOPE.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 组装实验参数
        set_params = {
            "qubits": qubit_name_list,
            "delay_start": args.delay_start,
            "delay_end": args.delay_end,
            "delay_sample_num": args.delay_sample_num,
            "step_height": args.step_height
        }

        # 新建实验记录，移除 pipeline_type
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[BASESLOPE] Task started run_id={run_id[:8]}")

        # 采集数据，使用新参数调用接口
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.BASESLOPE,
            qubits=qubit_name_list,
            delay_start=args.delay_start,
            delay_end=args.delay_end,
            delay_sample_num=args.delay_sample_num,
            step_height=args.step_height
        )

        # 读取原始数据（适配统一接口）
        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 写入原始数据
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 数据分析
        analysis_result = baseslope(raw_data)

        # 绘制波形图，统一图片命名规则
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/{CtrlTaskName.BASESLOPE.value}_{pure_name}_{run_id}.png'
        plot_baseslope(raw_data, analysis_result, save_path=img_save_path)
        plot_paths = [img_save_path]

        # 调用图片分析函数
        # llm_analysis(img_save_path)

        # 本任务无参数更新逻辑
        new_full_params = set_params.copy()

        # 更新结果到存储
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        logging.info(f"测量完成，参数： {new_full_params}")

    except Exception as e:
        err_msg = f"baseslope测量异常：{str(e)}"
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
    get_baseslope_hdf5_res(cli_args)