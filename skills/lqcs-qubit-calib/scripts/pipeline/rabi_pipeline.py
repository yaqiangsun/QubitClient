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
        python -m resources.lqcs.pipeline.rabi_pipeline -q q3lu7 -s ./tmp -u True -c 0.6
"""
import sys
import argparse
import uuid
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
from analysis.inception import rabi
from analysis.visualization import plot_rabicos

DEFAULT_SAVE_FOLDER = './tmp'

def parse_args():
    parser = argparse.ArgumentParser(description="Rabi Amplitude Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit list, default: q3lu7")
    parser.add_argument("--piamp-start", type=float, default=0, help="Pulse amplitude start")
    parser.add_argument("--piamp-end", type=float, default=2, help="Pulse amplitude end")
    parser.add_argument("--piamp-samples", type=int, default=20, help="Amplitude sample count")
    parser.add_argument("--pi-len", type=float, default=50, help="pi length")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    # 新增统一参数
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_rabi_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "rabi"
    pipeline_type = "rabi_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        # 1.采集数据
        qubit_ctrl_client = QubitCtrlClient()
        set_params = {
            "qubits": qubit_name_list,
            "amp_start": args.amp_start,
            "amp_end": args.amp_end,
            "amp_sample_num": args.amp_samples,
            "pi_len": args.pi_len
        }

        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[RABI] Task started run_id={run_id[:8]}")

        data = qubit_ctrl_client.run(CtrlTaskName.RABI,
                                       qubits=qubit_name_list,
                                       piamp_start=args.piamp_start,
                                       piamp_end=args.piamp_end,
                                       piamp_sample_num=args.piamp_samples,
                                       pi_len=args.pi_len
                                       )
        data_id = data[0]["text"]
        data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        data = json.loads(data[0]["text"])

        # 2.分析数据
        analysis_result = rabi(data)

        # 3.绘图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/rabi_{pure_name}.png'
        fig_list = plot_rabicos(data, analysis_result, save_path=img_save_path)

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
        # test_qubit_spectroscopy_q5_extract(img_small_path)
        # test_qubit_spectroscopy_q6_status(img_small_path)
        # print("\nQubit_Spectroscopy tests passed!")

        new_full_params = set_params.copy()
        update_amp_map = {}
        # 5.更新PiGate.amp
        # 根据扫描结果更新
        if type(analysis_result)==dict:
            if "results" not in analysis_result.keys():
                analysis_result = analysis_result.get("results")
            elif "result" in analysis_result.keys():
                analysis_result = analysis_result.get("result")

        # 增加更新开关与置信度判断
        if args.update:
            for result in analysis_result:
                peaks_list = result['peaks']
                confs_list = result['confs']
                for i in range(len(qubit_name_list)):
                    if i < len(peaks_list):
                        peaks = peaks_list[i]
                        confs = confs_list[i]
                        print("---confs: ", confs)
                        if confs:
                            max_conf = max(confs)
                            if max_conf < args.confidence:
                                continue
                            best_idx = confs.index(max_conf)
                            best_peak = peaks[best_idx]
                            target_amp =best_peak
                            values=str(target_amp)
                            qname=qubit_name_list[i]
                            task_type=CtrlTaskName.RABI
                            qubit_ctrl_client.update_param(qname=qname, task_type=task_type, values=values)
                            update_amp_map[qname] = target_amp
        if update_amp_map:
            new_full_params["pi_gate_amp"] = update_amp_map

        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=[img_save_path],
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        print(f"Measurement finished, updated params: {new_full_params}")

    except Exception as e:
        err_msg = f"Measure failed: {str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        print(f"Task failed run_id={run_id[:8]} error: {err_msg}")
        raise

if __name__ == '__main__':
    cli_args = parse_args()
    get_rabi_hdf5_res(cli_args)