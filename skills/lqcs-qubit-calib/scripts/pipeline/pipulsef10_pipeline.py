# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/16
########################################################################


"""PiPulseF10 measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: python -m tests.ui.serve
    2. cmd params example:
            python -m resources.lqcs.pipeline.pipulsef10_pipeline -q q3lu7 -dfs 0 -dfe 0.03 -dfn 21 -s ./tmp -u True -c 0.6
"""

import sys
import argparse
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

from analysis.inception import spectrum
from analysis.visualization import plot_spectrum

SAVE_PLOT_FOLDER = './tmp'


def parse_args():
    parser = argparse.ArgumentParser(description="PiPulseF10 Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit name list, default: q3lu7")
    # df起始
    parser.add_argument("--df-start", "-dfs", type=float, default=0,
                        help="Delta frequency start value, default 0")
    # df终止
    parser.add_argument("--df-end", "-dfe", type=float, default=0.03,
                        help="Delta frequency end value, default 0.03")
    # df采样点数
    parser.add_argument("--df-sample-num", "-dfn", type=int, default=21,
                        help="Delta frequency sampling count, default 21")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save spectrum plot image")
    # 新增更新开关、置信度阈值
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_pipulsef10_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "pipulsef10"
    pipeline_type = "pipulsef10_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    qname = qubit_name_list[0]

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 提前查询原始f10初始值，存入参数方便前端查看更新前原值
        f10_raw = qubit_ctrl_client.query_param(qname=qname, key="f10_star")
        f10_original = float(f10_raw[0]["text"])

        # 设置实验参数，加入更新前原始f10值
        set_params = {
            "qubits": qubit_name_list,
            "df_start": args.df_start,
            "df_end": args.df_end,
            "df_sample_num": args.df_sample_num,
            "f10": f10_original
        }

        # 新建实验记录，写入存储
        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[PiPulseF10] Task started run_id={run_id[:8]}, original f10={f10_original}")
    
        # =========== 采集数据 ===========
        data = qubit_ctrl_client.run(
            CtrlTaskName.PIPULSEF10,
            qubits=qubit_name_list,
            df_start=set_params["df_start"],
            df_end=set_params["df_end"],
            df_sample_num=set_params["df_sample_num"]
        )
        data_id = data[0]["text"]
        raw_data_text = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
        raw_data = json.loads(raw_data_text[0]["text"])

        # =========== 写入原始数据 ===========
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # =========== 分析 ============
        analysis_result = spectrum(raw_data)

        # =========== 绘制波形图==========
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/pipulsef10_{pure_name}.png'
        fig_list = plot_spectrum(raw_data, analysis_result, save_path=img_save_path)
        plot_paths = [img_save_path]

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

        # 5.更新f10, f21
        new_full_params = set_params.copy()
        freq_update_map = {}
        # 根据扫描结果更新
        if type(analysis_result)==dict:
            if "results" not in analysis_result.keys():
                analysis_result = analysis_result.get("results")
            elif "result" in analysis_result.keys():
                analysis_result = analysis_result.get("result")

        # 增加更新开关 + 置信度阈值判断
        if args.update:
            for result in analysis_result:
                peaks_list = result['peaks_list']
                confidences_list = result['confidences_list']
                for i in range(len(qubit_name_list)):
                    if i < len(peaks_list):
                        peaks = peaks_list[i]
                        confidences = confidences_list[i]
                        if len(confidences) > 0:
                            print("----confidences: ", confidences)
                            max_conf = max(confidences)
                            if max_conf < args.confidence:
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
        if freq_update_map:
            new_full_params["qubit_freq_calib"] = freq_update_map

        # =========== 更新结果到存储 ======================
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )

    except Exception as e:
        # ========== 捕获异常，存入错误信息 ================
        err_msg = f"PiPulseF10测量异常：{str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        print(f"任务失败 run_id={run_id[:8]} 错误：{err_msg}")
        raise


if __name__ == '__main__':
    cli_args = parse_args()
    get_pipulsef10_hdf5_res(cli_args)