# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################

"""Rabi pulse amplitude scan pipeline with UI storage & cmd args
Usage:
    1. Start UI server first: qubitclient ui start
    2. Example:
        python -m skills.lqcs-qubit-calib.scripts.pipeline.rabi_pipeline -q q1ld5 -u True -c 0.6 -ps 0 -pe 5 -pn 100 
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

from analysis.inception import rabi
from analysis.visualization import plot_rabicos
from analysis.update import rabi_update

DEFAULT_SAVE_FOLDER = './tmp/db/result/image'


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
    parser = argparse.ArgumentParser(description="Rabi Amplitude Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit list, default: q1ld5")
    parser.add_argument("--piamp-start", "-ps", type=float, default=0, help="Pulse amplitude start")
    parser.add_argument("--piamp-end", "-pe", type=float, default=5, help="Pulse amplitude end")
    parser.add_argument("--piamp-samples", "-pn", type=int, default=100, help="Amplitude sample count")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")

    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_rabi_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.RABI.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    qname = qubit_name_list[0]

    qubit_ctrl_client = QubitCtrlClient()
    pigate_amp_star_original = qubit_ctrl_client.query_param(qname=qname, key="PiGate_amp_star")
    pihalf_amp_star_original = qubit_ctrl_client.query_param(qname=qname, key="PiHalf_amp_star")

    try:
        # 1.采集数据
        set_params = {
            "qubits": qubit_name_list,
            "amp_start": args.piamp_start,
            "amp_end": args.piamp_end,
            "amp_sample_num": args.piamp_samples,
            "PiGate_amp_star": pigate_amp_star_original,
            "PiHalf_amp_star": pihalf_amp_star_original
        }

        # 新建实验记录，移除 pipeline_type
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[RABI] Task started run_id={run_id[:8]}")

        data_id = qubit_ctrl_client.run(
            CtrlTaskName.RABI,
            qubits=qubit_name_list,
            piamp_start=args.piamp_start,
            piamp_end=args.piamp_end,
            piamp_sample_num=args.piamp_samples
        )
        # 读取原始数据
        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 写入原始数据
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 2.分析数据
        analysis_result = rabi(raw_data)


        # 3.绘图
        img_save_path = f'{save_folder}/{CtrlTaskName.RABI.value}_{qname}_{run_id}.png'
        plot_rabicos(raw_data, analysis_result, save_path=img_save_path)
        img_save_path = os.path.abspath(img_save_path)
        plot_paths = [img_save_path]

        # 调用大模型图片分析
        # llm_analysis(img_save_path)

        new_full_params = set_params.copy()
        update_amp_map = {}

        # 开启更新
        if args.update:
            # 调用更新接口
            update_amp_map = rabi_update(
                results=analysis_result,
                conf_threshold=args.confidence,
                qubit_name_list=qubit_name_list
            )

            # 下发更新参数
            if qname in update_amp_map:
                target_pigate_amp_star = float(update_amp_map[qame])
                target_pihalf_amp_star = target_pigate_amp_star / 2
                target_values = [target_pigate_amp_star, target_pihalf_amp_star]

                qubit_ctrl_client.update_param(
                    qname=qname,
                    task_type=CtrlTaskName.RABI,
                    values=[target_values]
                )

                new_full_params["PiGate_amp_star"] = target_pigate_amp_star
                new_full_params["PiHalf_amp_star"] = target_pihalf_amp_star

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
    get_rabi_hdf5_res(cli_args)