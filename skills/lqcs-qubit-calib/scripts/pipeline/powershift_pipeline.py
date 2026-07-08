# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################

"""PowerShift scan pipeline with UI storage & cmd args
Usage:
    1. Start UI server first: qubitclient ui start
    2. Example:
        python -m skills.lqcs-qubit-calib.scripts.pipeline.powershift_pipeline -q q1ld5 -b 0.002 -n 15 -pn 20 -pe 0 -u True -c 0.3
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
import uuid
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

from analysis.inception import powershift
from analysis.visualization import plot_powershift
from analysis.update import powershift_update

DEFAULT_SAVE_FOLDER = './tmp/db/result/image'


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
    logging.info("Qubit_Spectroscopy tests passed!")


def parse_args():
    parser = argparse.ArgumentParser(description="PowerShift Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit list, default: q1ld5")
    parser.add_argument("--fread", "-f", type=float, default=None,
                        help="Manual readout freq(GHz), auto query hardware if empty")
    parser.add_argument("--bandwidth", "-b", type=float, default=0.0015,
                        help="Freq half bandwidth(GHz), default 0.0015")
    parser.add_argument("--samples", "-n", type=int, default=16, help="Freq sample count")
    parser.add_argument("--power-start", "-ps", type=float, default=-40, help="Drive power start")
    parser.add_argument("--power-end", "-pe", type=float, default=-16, help="Drive power end")
    parser.add_argument("--power-samples", "-pn", type=int, default=13, help="Power sample count")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    # 更新开关与置信度阈值
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_powershift_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.POWERSHIFT.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    qname = qubit_name_list[0]

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 获取读取频率
        if args.fread is not None:
            fread = args.fread
        else:
            fread_ret = qubit_ctrl_client.query_param(qname=qname, key="fread_star")
            fread = float(fread_ret)

        readin_power_original = qubit_ctrl_client.query_param(qname=qname, key="ReadIn_power_star")

        # 组装实验参数
        set_params = {
            "qubits": qubit_name_list,
            "frequency_center": fread,
            "frequency_half_bandwidth": args.bandwidth,
            "frequency_sample_num": args.samples,
            "power_start": args.power_start,
            "power_end": args.power_end,
            "power_sample_num": args.power_samples,
            "ReadIn_power_star": readin_power_original
        }

        # 新建实验记录，移除 pipeline_type
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[POWERSHIFT] Task started run_id={run_id[:8]}")

        # 采集数据
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.POWERSHIFT,
            qubits=qubit_name_list,
            freq_center=fread,
            freq_half_bandwidth=args.bandwidth,
            freq_sample_num=args.samples,
            power_start=args.power_start,
            power_end=args.power_end,
            power_sample_num=args.power_samples
        )

        # 读取原始数据
        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 写入原始数据
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 数据分析
        analysis_result = powershift(raw_data)

        # 绘图，统一命名规则
        img_save_path = f'{save_folder}/{CtrlTaskName.POWERSHIFT.value}_{qname}_{run_id}.png'
        plot_powershift(raw_data, analysis_result, save_path=img_save_path)
        img_save_path = os.path.abspath(img_save_path)
        plot_paths = [img_save_path]

        # 调用大模型图片分析
        # llm_analysis(img_save_path)

        new_full_params = set_params.copy()
        update_power_map = {}

        # 开启更新
        if args.update:

            # 调用独立更新函数
            update_power_map = powershift_update(
                results=analysis_result,
                conf_threshold=args.confidence,
                qubit_name_list=qubit_name_list
            )

            for q, target_power in update_power_map.items():
                qubit_ctrl_client.update_param(
                    qname=q,
                    task_type=CtrlTaskName.POWERSHIFT,
                    values=[target_power]
                )
                logging.info(f"[INFO] Update {q} power to {target_power}")

        if update_power_map:
            new_full_params["ReadIn_power_star"] = float(update_power_map[qname])

        # 结果入库
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        logging.info(f"Measurement finished, updated params: {new_full_params}")

    except Exception as e:
        err_msg = f"Measure failed: {str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        logging.error(f"Task failed run_id={run_id[:8]} error: {err_msg}")
        raise


if __name__ == '__main__':
    cli_args = parse_args()
    get_powershift_hdf5_res(cli_args)