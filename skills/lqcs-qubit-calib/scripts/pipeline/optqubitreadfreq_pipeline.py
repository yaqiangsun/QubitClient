# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/17
########################################################################


"""Opt Qubit Read Freq measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m skills.lqcs-qubit-calib.scripts.pipeline.optqubitreadfreq_pipeline -q q1ld5 -u True -c 0.6
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
from analysis.inception import optreadfreq
from analysis.visualization import plot_optreadfreq
from analysis.update import optreadfreq_update

DEFAULT_SAVE_FOLDER = './tmp'


def llm_analysis(img_save_path):
    # 图片缩放与大模型分析
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
    logging.info("\nQubit_Spectroscopy tests passed!")


def parse_args():
    parser = argparse.ArgumentParser(description="Opt Qubit Read Freq Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit name list, default: q1ld5")
    # 扫频半带宽
    parser.add_argument("--freq-half-bandwidth", "-h", type=float, default=0.0015,
                        help="Frequency span, default 0.0015")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Folder to save plot image")
    # 是否开启参数更新
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    # 置信度阈值
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_optqubitreadfreq_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.OPTQUBITREADFREQ.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    qname = qubit_name_list[0]

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 查询原始读取频率
        fread_raw = qubit_ctrl_client.query_param(qname=qname, key="fread_star")
        fread_original = float(fread_raw)
        logging.info(f"fread: {fread_original}")

        # 组装实验参数
        set_params = {
            "qubits": qubit_name_list,
            "freq_half_bandwidth": args.freq_half_bandwidth,
            "fread_star": fread_original
        }

        # 新建实验记录
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[OptReadFreq] Task started run_id={run_id[:8]}, original fread={fread_original}")

        # 采集数据
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.OPTQUBITREADFREQ,
            qubits=qubit_name_list,
            freq_half_bandwidth=set_params["freq_half_bandwidth"]
        )

        # 读取原始数据
        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 写入原始数据至存储
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 数据分析
        analysis_result = optreadfreq(raw_data)

        # 绘图保存，统一命名规则
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/{CtrlTaskName.OPTQUBITREADFREQ.value}_{pure_name}_{run_id}.png'
        plot_optreadfreq(raw_data, analysis_result, save_path=img_save_path)
        plot_paths = [img_save_path]

        # 调用大模型分析函数
        # llm_analysis(img_save_path)

        # 初始化新参数字典
        new_full_params = set_params.copy()

        # 开启更新则调用独立更新函数
        if args.update:
            update_map = optreadfreq_update(
                results=analysis_result,
                raw_data=raw_data,
                conf_threshold=args.confidence,
                qubit_name_list=qubit_name_list
            )
            # 更新参数
            for qname, info in update_map.items():
                new_val = info["fread_star"]
                qubit_ctrl_client.update_param(
                    qname=qname,
                    task_type=CtrlTaskName.OPTQUBITREADFREQ,
                    values=str(new_val)
                )
                new_full_params["fread_star"] = new_val

        # 更新结果存入存储
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )

    except Exception as e:
        err_msg = f"OptQubitReadFreq测量异常：{str(e)}"
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
    get_optqubitreadfreq_hdf5_res(cli_args)