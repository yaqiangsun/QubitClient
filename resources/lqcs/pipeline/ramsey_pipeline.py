# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################

"""Ramsey coherence scan pipeline with UI storage & cmd args
Usage:
    1. Start UI server first: python -m tests.ui.serve
    2. Example:
        python -m resources.lqcs.pipeline.ramsey_pipeline -q q3lu7 -s ./tmp -u True -c 0.6
"""
import sys
import argparse
import uuid
import math
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
from analysis.inception import ramsey
from analysis.visualization import plot_ramsey

DEFAULT_SAVE_FOLDER = './tmp'

def parse_args():
    parser = argparse.ArgumentParser(description="Ramsey Coherence Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit list, default: q3lu7")
    parser.add_argument("--fringe-freq", type=float, default=0.05, help="Ramsey fringe frequency")
    parser.add_argument("--delay-start", type=float, default=0, help="Delay start")
    parser.add_argument("--delay-end", type=float, default=100, help="Delay end")
    parser.add_argument("--delay-samples", type=int, default=100, help="Delay sample count")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    # 新增更新开关与置信度阈值
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()

def get_ramsey_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "ramsey"
    pipeline_type = "ramsey_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    fringeFreq = args.fringe_freq

    try:
        # 1.采集数据
        qubit_ctrl_client = QubitCtrlClient()
        set_params = {
            "qubits": qubit_name_list,
            "delay_start": args.delay_start,
            "delay_end": args.delay_end,
            "delay_sample_num": args.delay_samples,
            "fringeFreq": fringeFreq
        }

        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[RAMSEY] Task started run_id={run_id[:8]}")

        data = qubit_ctrl_client.run(CtrlTaskName.RAMSEY,
                                       qubits=qubit_name_list,
                                       delay_start=args.delay_start,
                                       delay_end=args.delay_end,
                                       delay_sample_num=args.delay_samples,
                                       fringeFreq=fringeFreq)
        data_id = data[0]["text"]
        data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        data = json.loads(data[0]["text"])

        # 2.分析数据
        analysis_result = ramsey(data)

        # 3.绘图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/ramsey_{pure_name}.png'
        fig_list = plot_ramsey(data, analysis_result, save_path=img_save_path)

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
        if type(analysis_result)==dict:
            if "results" not in analysis_result.keys():
                analysis_result = analysis_result.get("results")
            elif "result" in analysis_result.keys():
                analysis_result = analysis_result.get("result")

        # 增加更新总开关
        if args.update:
            for result in analysis_result:
                print("----", result.keys())
                params_list = result['params_list']
                r2_list = result['r2_list']
                fit_data_list = result['fit_data_list']
                confs_list = result['confs_list']
                for i in range(len(qubit_name_list)):
                    if i < len(params_list):
                        params = params_list[i]
                        # conf = confs_list[i] # no conf exist
                        # if conf < args.confidence:
                        #     continue
                        w = params[4]
                        qname=qubit_name_list[i]
                        task_type=CtrlTaskName.RAMSEY
                        f10 = qubit_ctrl_client.query_param(qname=qname, key="f10_star")
                        f10 = float(f10[0]["text"])
                        deltaf = w /(2*math.pi)         # 失谐量（Hz）
                        print("fringeFreq, f10: ", fringeFreq, f10)
                        if(fringeFreq>f10):
                            target_freq = fringeFreq - deltaf    # 如果 f_measure > f10
                        
                        else:
                             target_freq = fringeFreq + deltaf    # 如果 f_measure < f10
                        non=-0.2
                        values=str(target_freq) + ',' + str(target_freq + non)
                        task_type=CtrlTaskName.RAMSEY
                        qubit_ctrl_client.update_param(qname=qname, task_type=task_type, values=values)
                        freq_update_map[qname] = {"f10": target_freq, "f21": target_freq + non}
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


if __name__ == '__main__':
    cli_args = parse_args()
    get_ramsey_hdf5_res(cli_args)