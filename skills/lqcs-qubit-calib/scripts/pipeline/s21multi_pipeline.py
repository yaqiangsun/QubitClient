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
    1. Start UI server first: qubitclient ui start
    2. Example:
        python -m resources.lqcs.pipeline.s21multi_pipeline -q q3lu7 -s ./tmp -u True -c 0.4 -r 0.0005 -fs 6.5 -fe 6.8
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

# 加载fread配置文件
CONFIG_PATH = "qubit_base_freq.json"
try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        base_freq_dict = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"配置文件不存在，请检查路径: {CONFIG_PATH}")



def parse_args():
    parser = argparse.ArgumentParser(description="Multi Qubit S21 Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit list, default: q3lu7")
    parser.add_argument("--freq-start", "-fs",type=float, default=6.5, help="Scan freq start GHz")
    parser.add_argument("--freq-end", "-fe",type=float, default=6.7, help="Scan freq end GHz")
    parser.add_argument("--sample-rate", "-r", type=float, default=0.0002, help="Frequency sample step")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    # 新增：是否开启参数更新
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    # 新增：置信度阈值
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()

def get_s21multi_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "s21multi"
    pipeline_type = "s21multi_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    qname = qubit_name_list[0]
    base_freq = base_freq_dict.get(qname)

    try:
        qubit_ctrl_client = QubitCtrlClient()
        set_params = {
            "qubits": qubit_name_list,
            "frequency_start": args.freq_start,
            "frequency_end": args.freq_end,
            "frequency_sample_rate": args.sample_rate,
            "fread": base_freq
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

        new_full_params = set_params.copy()
        update_map = {}

        # 解析分析结果
        if isinstance(analysis_result, dict):
            if "results" in analysis_result:
                analysis_result = analysis_result.get("results")
            elif "result" in analysis_result:
                analysis_result = analysis_result.get("result")

        # 仅开启更新时，执行参数更新逻辑
        if args.update:
            for result in analysis_result:
                peaks_list = result['peaks']
                confs_list = result['confs']
                freqs_list = result['freqs_list']
                for i in range(len(qubit_name_list)):
                    # peaks = peaks_list[i]
                    confs = confs_list[i]
                    print("confs: ", confs)
                    freqs = freqs_list[i]
                    qname = qubit_name_list[i]
                    base_freq = base_freq_dict.get(qname)

                    if len(freqs) and len(confs):
                        # 置信度大于阈值才执行更新
                        idx = freqs.index(min(freqs, key=lambda f: abs(f - base_freq)))
                        closest_freq = freqs[idx]
                        cur_conf = float(confs[idx])
                        if cur_conf > args.confidence:
                            print("[INFO] update : ", closest_freq, qname)
                            update_map[qname] = closest_freq
                            qubit_ctrl_client.update_param(qname=qname, task_type=CtrlTaskName.S21MULTI, values=str(closest_freq))

        if update_map:
            new_full_params["fread"] = update_map

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