# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiangsun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/18
########################################################################


"""SpinEcho T2 measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m skills.lqcs-qubit-calib.scripts.pipeline.spinecho_t2_pipeline -q q1ld4 -ff 0.05 -ds 0 -de 10000 -dn 50 -s ./tmp
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
import json
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

from analysis.inception import spinecho
from analysis.visualization import plot_spinecho

SAVE_PLOT_FOLDER = './tmp'


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
    # test_qubit_spectroscopy_q5_extract(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    logging.info("Qubit_Spectroscopy tests passed!")


def parse_args():
    parser = argparse.ArgumentParser(description="SpinEcho T2 Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld4"],
                        help="Target qubit name list, default: q1ld4")

    # 延时起始值
    parser.add_argument("--delay-start", "-ds", type=float, default=0,
                        help="Delay start value, default 0")
    # 延时终止值
    parser.add_argument("--delay-end", "-de", type=float, default=10000,
                        help="Delay end value, default 10000")
    # 延时采样点数
    parser.add_argument("--delay-sample-num", "-dn", type=int, default=200,
                        help="Delay sampling count, default 200")
    # 条纹频率
    parser.add_argument("--fringe-freq", "-ff", type=float, default=0.005,
                        help="Fringe frequency, default 0.05")
    # pipulse_num
    parser.add_argument("--pipulse_num", "-m", type=float, default=1,
                        help="ma, default None")

    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save plot image")
    return parser.parse_args()


def get_t2_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.SPINECHO_T2.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 组装实验参数
        set_params = {
            "qubits": qubit_name_list,
            "fringeFreq": args.fringe_freq,
            "delay_start": args.delay_start,
            "delay_end": args.delay_end,
            "delay_sample_num": args.delay_sample_num,
            "pipulse_num": args.pipulse_num
        }

        # 新建实验记录并入库
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[SpinEcho T2] Task started run_id={run_id[:8]}")

        # 1.采集数据
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.SPINECHO_T2,
            qubits=qubit_name_list,
            delay_start=args.delay_start,
            delay_end=args.delay_end,
            delay_sample_num=args.delay_sample_num,
            fringeFreq=args.fringe_freq,
            pipulse_num=args.pipulse_num
        )
        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 写入原始数据ID与原始数据
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 2.分析数据
        analysis_result = spinecho(raw_data)

        # 3.绘图
        img_save_path = f'{save_folder}/{CtrlTaskName.SPINECHO_T2.value}_{qubit_name_list[0]}_{run_id}.png'
        fig_list = plot_spinecho(raw_data, analysis_result, save_path=img_save_path)

        # 按需开启图片处理
        # llm_analysis(img_save_path)

        # 5.无参数更新

        # 写入完成状态、分析结果、图片路径
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=[img_save_path],
            completed_at=datetime.now(),
            new_params=set_params
        )
        logging.info("SpinEcho T2 测量完成")

    except Exception as e:
        # 异常捕获并记录
        err_msg = f"SpinEcho T2 测量异常：{str(e)}"
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
    get_t2_hdf5_res(cli_args)