# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/15
########################################################################


"""2D spectrum measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
    faster: python -m resources.lqcs.pipeline.spectrum2d_pipeline -q q3lu7 -fs -3 -fe 3 -fn 10 -bs -1 -be 1 -bn 10 -da 0.0 -s ./tmp -u True -c 0.6

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

from analysis.inception import nnspectrum2d
from analysis.visualization import plot_nnspectrum2d

SAVE_PLOT_FOLDER = './tmp'


def parse_args():
    parser = argparse.ArgumentParser(description="2D Spectrum Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit name list, default: q3lu7")
    # 频率起始
    parser.add_argument("--freq-start", "-fs", type=float, default=3,
                        help="Frequency start value, default 3")
    # 频率终止
    parser.add_argument("--freq-end", "-fe", type=float, default=5,
                        help="Frequency end value, default 5")
    # 频率采样点数
    parser.add_argument("--freq-sample-num", "-fn", type=int, default=100,
                        help="Frequency sampling count, default 200")
    # 偏置起始
    parser.add_argument("--zpa-start", "-zs", type=float, default=-1,
                        help="zpa start value, default -1")
    # 偏置终止
    parser.add_argument("--zpa-end", "-ze", type=float, default=1,
                        help="zpa end value, default 1")
    # 偏置采样点数
    parser.add_argument("--zpa-sample-num", "-zn", type=int, default=100,
                        help="zpas sampling count, default 200")
    # 幅度
    parser.add_argument("--spec-amp", "-sa", type=float, default=0.5,
                        help="Spec amplitude, default 0.0")
    # 频率
    parser.add_argument("--sb_freq", "-sa", type=float, default=-0.15,
                        help="sb_freq, default -0.15")
    
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save spectrum plot image")
    # 新增：是否开启参数更新
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    # 新增：置信度阈值
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_spectrum2d_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "spectrum2d"
    pipeline_type = "spectrum2d_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 设置实验参数
        set_params = {
            "qubits": qubit_name_list,
            "freq_start": args.freq_start,
            "freq_end": args.freq_end,
            "freq_sample_num": args.freq_sample_num,
            "zpa_start": args.zpa_start,
            "zpa_end": args.zpa_end,
            "zpa_sample_num": args.zpa_sample_num,
            "spec_amp": args.spec_amp,
            "sb_freq": args.sb_freq
        }

        # 新建实验记录，写入存储
        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[Spectrum2D] Task started run_id={run_id[:8]}")

        
        data = qubit_ctrl_client.run(
            CtrlTaskName.SPECTRUM_2D,
            qubits=qubit_name_list,
            freq_start=set_params["freq_start"],
            freq_end=set_params["freq_end"],
            freq_sample_num=set_params["freq_sample_num"],
            zpa_start=set_params["zpa_start"],
            zpa_end=set_params["zpa_end"],
            zpa_sample_num=set_params["zpa_sample_num"],
            spec_amp=set_params["spec_amp"],
            sb_freq=set_params["sb_freq"]
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
        analysis_result = nnspectrum2d(raw_data)
        

        # =========== 绘制波形图==========
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/spectrum2d_{pure_name}.png'
        fig_list = plot_nnspectrum2d(raw_data, analysis_result, save_path=img_save_path)
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

        # =========== 参数更新逻辑 ===========
        new_full_params = set_params.copy()
        update_map = {}

        # 解析分析结果
        if isinstance(analysis_result, dict):
            if "results" in analysis_result:
                analysis_result = analysis_result.get("results")
            elif "result" in analysis_result:
                analysis_result = analysis_result.get("result")

        # 暫時沒有參數更新


        # =========== 更新结果到存储 ======================
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        print(f"测量完成，参数： {new_full_params}")

    except Exception as e:
        # ========== 捕获异常，存入错误信息 ================
        err_msg = f"2D频谱测量异常：{str(e)}"
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
    get_spectrum2d_hdf5_res(cli_args)