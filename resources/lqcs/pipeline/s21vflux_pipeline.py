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
    1. Start UI server first: python -m tests.ui.serve
    2. Example:
        python -m resources.lqcs.pipeline.s21vflux_pipeline -q q3lu7 -b 0.001 -n 11 -s ./tmp
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
    parser.add_argument("--bandwidth", "-b", type=float, default=0.001,
                        help="Freq half bandwidth(GHz), default 0.001")
    parser.add_argument("--samples", "-n", type=int, default=11,
                        help="Freq sample count, default 11")
    parser.add_argument("--bias-start", type=float, default=-3, help="Flux bias start")
    parser.add_argument("--bias-end", type=float, default=3, help="Flux bias end")
    parser.add_argument("--bias-samples", type=int, default=16, help="Bias sample count")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
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

        # LLM image analyze reserved code
        # img_small_path = img_save_path.split('.png')[0] + '_small.png'
        # with Image.open(img_save_path) as img:
        #     w, h = img.size
        #     new_w = w // 10
        #     new_h = h // 10
        #     img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        #     img_small.save(img_small_path, dpi=(300, 300))

        new_full_params = set_params.copy()
        updated_bias = None
        if isinstance(analysis_result, dict):
            if "results" not in analysis_result:
                analysis_result = analysis_result.get("results")
            elif "result" in analysis_result:
                analysis_result = analysis_result.get("result")

        for result in analysis_result:
            coscurves_list = result['coscurves_list']
            cosconfs_list = result['cosconfs_list']
            for i in range(len(qubit_name_list)):
                coscurves = coscurves_list[i]
                cosconfs = cosconfs_list[i]
                if not cosconfs:
                    print(f"[WARN] No valid peak for qubit {qubit_name_list[i]}, skip bias update")
                    continue
                best_idx = cosconfs.index(max(cosconfs))
                best_curve = coscurves[best_idx]
                y_vals = [y for x, y in best_curve]
                index_max_y = y_vals.index(max(y_vals))
                half_index = index_max_y // 2
                target_bias = best_curve[half_index][0]
                updated_bias = target_bias
                curr_q = qubit_name_list[i]
                qubit_ctrl_client.update_param(qname=curr_q, task_type=CtrlTaskName.S21VSFLUX, values=str(target_bias))
        if updated_bias is not None:
            new_full_params["read_bias"] = updated_bias

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
    get_s21vflux_hdf5_res(cli_args)