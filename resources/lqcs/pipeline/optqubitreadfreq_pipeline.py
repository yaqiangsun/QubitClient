# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/17
########################################################################


"""Opt Qubit Read Freq measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: python -m tests.ui.serve
    2. cmd params example:
            python -m resources.lqcs.pipeline.optqubitreadfreq_pipeline -q q3lu7 -sp 0.0055 -s ./tmp
"""

import sys
import argparse
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

from analysis.inception import optreadfreq
from analysis.visualization import plot_optreadfreq

SAVE_PLOT_FOLDER = './tmp'


def parse_args():
    parser = argparse.ArgumentParser(description="Opt Qubit Read Freq Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit name list, default: q3lu7")
    # 扫频半带宽
    parser.add_argument("--freq-span", "-sp", type=float, default=0.0055,
                        help="Frequency span, default 0.0055")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save plot image")
    return parser.parse_args()


def get_optqubitreadfreq_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "optqubitreadfreq"
    pipeline_type = "optqubitreadfreq_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    qname = qubit_name_list[0]

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 查询原始读取频率
        fread_raw = qubit_ctrl_client.query_param(qname=qname, key="fread_star")
        fread_original = float(fread_raw[0]["text"])
        print("----------fread_original: ", fread_original)

        # 组装实验参数
        set_params = {
            "qubits": qubit_name_list,
            "freq_span": args.freq_span,
            "fread": fread_original
        }

        # 新建实验记录存入存储
        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[OptReadFreq] Task started run_id={run_id[:8]}, original fread={fread_original}")

        # =========== 采集数据 ===========
        data = qubit_ctrl_client.run(
            CtrlTaskName.OPTQUBITREADFREQ,
            qubits=qubit_name_list,
            freq_span=set_params["freq_span"]
        )
        data_id = data[0]["text"]
        raw_data_text = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
        raw_data = json.loads(raw_data_text[0]["text"])

        # 写入原始数据至存储
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # =========== 数据分析 ===========
        analysis_result = optreadfreq(raw_data)

        # =========== 绘图保存 ===========
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/optqubitreadfreq_{pure_name}.png'
        fig_list = plot_optreadfreq(raw_data, analysis_result, save_path=img_save_path)
        plot_paths = [img_save_path]

        # =========== 大模型分析===========
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

        analysis_data = analysis_result
        if isinstance(analysis_data, dict):
            if "results" in analysis_data:
                analysis_data = analysis_data["results"]
            elif "result" in analysis_data:
                analysis_data = analysis_data["result"]

        # 初始化更新后的新参数字典
        new_full_params = set_params.copy()
        updated_freq = None

        data_content = raw_data['q3lu7']

        for result in analysis_data:
            freqs_list = result['peak_list']
            for idx in range(len(qubit_name_list)):
                freqs = freqs_list[idx]
                curr_q = qubit_name_list[idx]

                updated_freq = str(data_content[freqs][0])
                # 更新寄存器
                qubit_ctrl_client.update_param(
                    qname=curr_q,
                    task_type=CtrlTaskName.OPTQUBITREADFREQ,
                    values=updated_freq
                )

                new_full_params["fread"] = float(updated_freq)



        # 更新参数存入存储
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )

    except Exception as e:
        # 异常捕获，写入存储标记失败
        err_msg = f"OptQubitReadFreq测量异常：{str(e)}"
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
    get_optqubitreadfreq_hdf5_res(cli_args)