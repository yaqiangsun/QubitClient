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
        faster: python -m qcontrol.lqcs-qubit-calib.scripts.pipeline.spectrum_2d_pipeline
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
import os
import numpy as np
import logging

# 统一日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import nnspectrum2d
from analysis.visualization import plot_nnspectrum2d

SAVE_PLOT_FOLDER ='./tmp/db/result/image'

def llm_analysis(img_save_path):
    # resize更小
    img_small_path = img_save_path.split('.png')[0] + '_small.png'
    logging.info(f"img_small_path: {img_small_path}")

    with Image.open(img_save_path) as img:
        w, h = img.size
        new_w = w // 10
        new_h = h // 10
        logging.info(f"size: {new_w}, {new_h}")
        img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img_small.save(img_small_path, dpi=(300, 300))

    # test_qubit_spectroscopy_q1_describe(img_small_path)
    # test_qubit_spectroscopy_q2_classify(img_small_path)
    # test_qubit_spectroscopy_q3_reasoning(img_small_path)
    # test_qubit_spectroscopy_q4_assess(img_small_path)
    # test_qubit_spectroscopy_q5_extract(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    logging.info("Qubit_Spectroscopy tests passed!")


def parse_args():
    parser = argparse.ArgumentParser(description="2D Spectrum Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit name list, default: q1ld5")
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
    # 边带频率
    parser.add_argument("--sb-freq", "-bf", type=float, default=-0.15,
                        help="sb_freq, default -0.15")

    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save spectrum plot image")
    # 是否开启参数更新
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    # 置信度阈值
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_spectrum2d_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.SPECTRUM_2D.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    qname = qubit_name_list[0]

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

        # 新建实验记录，移除 pipeline_type
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[Spectrum2D] Task started run_id={run_id[:8]}")

        data_id = qubit_ctrl_client.run(
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

        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
        

        # 写入原始数据
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 数据分析
        analysis_result = nnspectrum2d(raw_data)

        # 绘图
        # pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/{CtrlTaskName.SPECTRUM_2D.value}_{qname}_{run_id}.png'
        fig_list = plot_nnspectrum2d(raw_data, analysis_result, save_path=img_save_path)

        img_save_path = os.path.abspath(img_save_path)
        plot_paths = [img_save_path]

        # Large Model
        # llm_analysis(img_save_path)

        # 当前无更新逻辑
        new_full_params = set_params.copy()

        # 结果入库
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        logging.info(f"测量完成，参数： {new_full_params}")

    except Exception as e:
        err_msg = f"2D频谱测量异常：{str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        logging.error(f"任务失败 run_id={run_id[:8]} 错误：{err_msg}")
        raise


if __name__ == '__main__':
    cli_args = parse_args()
    get_spectrum2d_hdf5_res(cli_args)