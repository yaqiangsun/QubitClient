# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################

"""Qubit Spectrum scan pipeline with UI storage & cmd args
Usage:
    1. Start UI server first: qubitclient ui start
    2. Example:
        python -m resources.lqcs.pipeline.spectrum_pipeline -q q3lu7 -s ./tmp -u True -c 0.6
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
from analysis.inception import nnspectrum
from analysis.visualization import plot_nnspectrum

DEFAULT_SAVE_FOLDER = './tmp'

def parse_args():
    parser = argparse.ArgumentParser(description="Qubit Spectrum Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit list, default: q3lu7")
    parser.add_argument("--freq-start", type=float, default=3.0, help="Scan freq start")
    parser.add_argument("--freq-end", type=float, default=5.0, help="Scan freq end")
    parser.add_argument("--freq-samples", type=int, default=1000, help="Frequency sample count")
    parser.add_argument("--zpa", type=float, default=0, help="Zpa value")
    parser.add_argument("--spec-amp", type=float, default=0.5, help="spec amplitude")
    parser.add_argument("--sb_freq", type=float, default=-0.15, help="sb_freq")

    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    # 新增更新开关与置信度阈值
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()

def get_spectrum_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "spectrum"
    pipeline_type = "spectrum_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        # 1.采集数据
        qubit_ctrl_client = QubitCtrlClient()
        set_params = {
            "qubits": qubit_name_list,
            "freq_start": args.freq_start,
            "freq_end": args.freq_end,
            "freq_sample_num": args.freq_samples,
            "zpa": args.zpa,
            "spec_amp": args.spec_amp,
            "sb_freq": args.sb_freq
        }

        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[SPECTRUM] Task started run_id={run_id[:8]}")
        
        data = qubit_ctrl_client.run(CtrlTaskName.SPECTRUM,
                                       qubits=qubit_name_list,
                                       freq_start=args.freq_start,
                                       freq_end=args.freq_end,
                                       freq_sample_num=args.freq_samples,
                                       zpa=args.zpa,
                                       spec_amp=args.spec_amp,
                                       sb_freq=args.sb_freq)
        data_id = data[0]["text"]
        data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        data = json.loads(data[0]["text"])

        # 2.分析数据
        analysis_result = nnspectrum(data)

        # 3.绘图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/spectrum_{pure_name}.png'
        fig_list = plot_nnspectrum(data, analysis_result, save_path=img_save_path)

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
        freq_update_map = {}
        # 5.更新f10, f21
        # 根据扫描结果更新
        if type(analysis_result)==dict:
            if "results" not in analysis_result.keys():
                analysis_result = analysis_result.get("results")
            elif "result" in analysis_result.keys():
                analysis_result = analysis_result.get("result")

        # 仅开启更新时执行参数更新逻辑
        if args.update:
            for result in analysis_result:
                peaks_list = result['peaks_list']
                confidences_list = result['confidences_list']
                for i in range(len(qubit_name_list)):
                    if i < len(peaks_list):
                        peaks = peaks_list[i]
                        confidences = confidences_list[i]
                        if len(confidences) > 0:
                            print("------confidences: ", confidences)
                            max_conf = max(confidences)
                            # 置信度低于阈值则跳过
                            if max_conf <= args.confidence:
                                continue
                            
                            best_idx = confidences.index(max_conf)
                            best_peak = peaks[best_idx]
                            target_freq =best_peak
                            non=-0.2
                            values=str(target_freq) + ',' + str(target_freq + non)
                            qname=qubit_name_list[i]
                            task_type=CtrlTaskName.SPECTRUM
                            qubit_ctrl_client.update_param(qname=qname, task_type=task_type, values=values)
                            freq_update_map[qname] = {"f10": target_freq, "f21": target_freq + non}
                            print(f"[INFO] Update {qname} freq, confidence: {max_conf}")

        if freq_update_map:
            new_full_params["qubit_freq_calib"] = freq_update_map

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
    get_spectrum_hdf5_res(cli_args)