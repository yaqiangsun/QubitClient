# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################

"""Multi-qubit S21 scan pipeline with UI storage & cmd args
Usage:
    1. Start UI server first: python -m tests.ui.serve
    2. Example:
        python -m resources.lqcs.pipeline.s21multi_pipeline -q q3lu7 -s ./tmp
"""
import sys
import argparse
import uuid
from datetime import datetime
from pathlib import Path
from PIL import Image
import json

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
from analysis.inception import nns21multi, s21multi
from analysis.visualization import plot_nns21multi, plot_s21multi

DEFAULT_SAVE_FOLDER = './tmp'

base_freq_dict = {
    'q1lu7': 6.561,
    'q2lu7': 6.759,
    'q3lu7': 6.590,
    'q4lu7': 6.762,
    'q5lu7': 6.539,
    'q6lu7': 6.763,
    'q7lu7': 6.611,
    'q8lu7': 6.803,
    'q9lu7': 6.634,
    'q10lu7': 6.855,
    'q11lu7': 6.666,
    'q12lu7': 6.876,
}

def parse_args():
    parser = argparse.ArgumentParser(description="Multi Qubit S21 Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit list, default: q3lu7")
    parser.add_argument("--freq-start", type=float, default=6.5, help="Scan freq start GHz")
    parser.add_argument("--freq-end", type=float, default=6.8, help="Scan freq end GHz")
    parser.add_argument("--sample-rate", type=float, default=0.0002, help="Frequency sample step")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    return parser.parse_args()

def get_s21multi_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "s21multi"
    pipeline_type = "s21multi_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        qubit_ctrl_client = QubitCtrlClient()
        set_params = {
            "qubits": qubit_name_list,
            "frequency_start": args.freq_start,
            "frequency_end": args.freq_end,
            "frequency_sample_rate": args.sample_rate
        }

        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[S21MULTI] Task started run_id={run_id[:8]}")

        data = qubit_ctrl_client.run(
            CtrlTaskName.S21MULTI,
            qubits=qubit_name_list,
            frequency_start=args.freq_start,
            frequency_end=args.freq_end,
            frequency_sample_rate=args.sample_rate
        )
        data_id = data[0]["text"]
        raw_data_text = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
        raw_data = json.loads(raw_data_text[0]["text"])

        store.update_run(run_id=run_id, raw_data_id=data_id, raw_data=raw_data)

        analysis_result = s21multi(raw_data)

        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/s21multi_{pure_name}.png'
        fig_list = plot_s21multi(raw_data, analysis_result, save_path=img_save_path)

        # LLM image analyze reserved code
        # img_small_path = img_save_path.split('.png')[0] + '_small.png'
        # with Image.open(img_save_path) as img:
        #     w, h = img.size
        #     new_w = w // 10
        #     new_h = h // 10
        #     img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        #     img_small.save(img_small_path, dpi=(300, 300))

        new_full_params = set_params.copy()
        update_map = {}
        if isinstance(analysis_result, dict):
            if "results" not in analysis_result:
                analysis_result = analysis_result.get("results")
            elif "result" in analysis_result:
                analysis_result = analysis_result.get("result")

        for result in analysis_result:
            peaks_list = result['peaks']
            confs_list = result['confs']
            freqs_list = result['freqs_list']
            for i in range(len(qubit_name_list)):
                peaks = peaks_list[i]
                confs = confs_list[i]
                freqs = freqs_list[i]
                qname = qubit_name_list[i]
                base_freq = base_freq_dict.get(qname)
                if len(freqs):
                    closest_freq = min(freqs, key=lambda f: abs(f - base_freq))
                    print("[INFO] update : ", closest_freq, qname)
                    update_map[qname] = closest_freq
                    qubit_ctrl_client.update_param(qname=qname, task_type=CtrlTaskName.S21MULTI, values=str(closest_freq))
        if update_map:
            new_full_params["qubit_freq_calib"] = update_map

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
    get_s21multi_hdf5_res(cli_args)