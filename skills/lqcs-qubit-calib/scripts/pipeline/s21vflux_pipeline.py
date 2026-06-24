# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################

"""S21 vs Flux 2D scan pipeline with UI storage & cmd args
Usage:
    1. Start UI server first: qubitclient ui start
    2. Example:
        python -m resources.lqcs.pipeline.s21vflux_pipeline -q q3lu7 -b 0.001 -n 11 -s ./tmp -u True -c 0.4
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
from analysis.inception import s21vsflux
from analysis.visualization import plot_s21vsflux

DEFAULT_SAVE_FOLDER = './tmp'

def parse_args():
    parser = argparse.ArgumentParser(description="S21VSFLUX 2D Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit list, default: q3lu7")
    parser.add_argument("--fread", "-f", type=float, default=None,
                        help="Manual readout freq(GHz), auto query hardware if empty")
    parser.add_argument("--bandwidth", "-b", type=float, default=0.03,
                        help="Freq half bandwidth(GHz), default 0.001")
    parser.add_argument("--samples", "-n", type=int, default=11,
                        help="Freq sample count, default 11")
    parser.add_argument("--bias-start", type=float, default=-3, help="Flux bias start")
    parser.add_argument("--bias-end", type=float, default=3, help="Flux bias end")
    parser.add_argument("--bias-samples", type=int, default=16, help="Bias sample count")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    # 新增更新开关与置信度阈值
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()

def get_s21vflux_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "s21vsflux"
    pipeline_type = "s21vsflux_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        qubit_ctrl_client = QubitCtrlClient()
        qname = qubit_name_list[0]
        task_type = CtrlTaskName.S21VSFLUX

        if args.fread is not None:
            fread = args.fread
        else:
            fread_ret = qubit_ctrl_client.query_param(qname=qname, key="fread_star")
            fread = float(fread_ret[0]["text"])

        set_params = {
            "qubits": qubit_name_list,
            "frequency_half_bandwidth": args.bandwidth,
            "frequency_sample_num": args.samples,
            "frequency_center": fread,
            "read_bias_start": args.bias_start,
            "read_bias_end": args.bias_end,
            "read_bias_sample_num": args.bias_samples
        }

        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[S21VSFLUX] Task started run_id={run_id[:8]}")

        data = qubit_ctrl_client.run(
            CtrlTaskName.S21VSFLUX,
            qubits=qubit_name_list,
            freq_center=fread,
            freq_half_bandwidth=args.bandwidth,
            freq_sample_num=args.samples,
            read_bias_start=args.bias_start,
            read_bias_end=args.bias_end,
            read_bias_sample_num=args.bias_samples
        )
        data_id = data[0]["text"]
        raw_data_text = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
        raw_data = json.loads(raw_data_text[0]["text"])

        store.update_run(run_id=run_id, raw_data_id=data_id, raw_data=raw_data)

        analysis_result = s21vsflux(raw_data)

        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/s21vflux_{pure_name}.png'
        fig_list = plot_s21vsflux(raw_data, analysis_result, save_path=img_save_path)

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

        # 不更新参数

        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=[img_save_path],
            completed_at=datetime.now(),
        )


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
    get_s21vflux_hdf5_res(cli_args)