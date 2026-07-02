# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiangsun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/16
########################################################################


"""XEB measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m skills.lqcs-qubit-calib.scripts.pipeline.xeb_pipeline -q q1ld4 -ms 0 -me 400 -mn 20 -k 10 -g reference -tb 0 -st 100 -s ./tmp
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
import json
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

from analysis.inception import xeb
from analysis.visualization import plot_xeb

SAVE_PLOT_FOLDER = './tmp'


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
    parser = argparse.ArgumentParser(description="XEB Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld4"],
                        help="Target qubit name list, default: q1ld4")
    # m起始
    parser.add_argument("--m-start", "-ms", type=int, default=0,
                        help="M start value, default 0")
    # m终止
    parser.add_argument("--m-end", "-me", type=int, default=400,
                        help="M end value, default 400")
    # m采样点数
    parser.add_argument("--m-sample-num", "-mn", type=int, default=10,
                        help="M sampling count, default 10")
    # k值
    parser.add_argument("--k", "-k", type=int, default=30,
                        help="XEB k param, default 30")
    # gate类型
    parser.add_argument("--gate", "-g", type=str, default="reference",
                        help="Gate type, default reference")
    # tbuffer
    parser.add_argument("--tbuffer", "-tb", type=int, default=0,
                        help="Time buffer, default 0")
    # 采样统计次数
    parser.add_argument("--stats", "-st", type=int, default=300,
                        help="Measurement stats count, default 300")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save spectrum plot image")
    return parser.parse_args()


def get_xeb_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.XEB.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        qubit_ctrl_client = QubitCtrlClient()

        # 设置实验参数
        set_params = {
            "qubits": qubit_name_list,
            "m_start": args.m_start,
            "m_end": args.m_end,
            "m_sample_num": args.m_sample_num,
            "k": args.k,
            "gate": args.gate,
            "tbuffer": args.tbuffer,
            "stats": args.stats
        }

        # 新建实验记录，移除 pipeline_type
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[XEB] Task started run_id={run_id[:8]}")

        # 采集数据
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.XEB,
            qubits=qubit_name_list,
            m_start=set_params["m_start"],
            m_end=set_params["m_end"],
            m_sample_num=set_params["m_sample_num"],
            k=set_params["k"],
            gate=set_params["gate"],
            tbuffer=set_params["tbuffer"],
            stats=set_params["stats"]
        )

        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 写入原始数据
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 分析数据
        analysis_result = xeb(raw_data)

        # 绘图
        img_save_path = f'{save_folder}/{CtrlTaskName.XEB.value}_{qubit_name_list[0]}_{run_id}.png'
        fig_list = plot_xeb(raw_data, analysis_result, save_path=img_save_path)

        # 大模型分析
        # llm_analysis(img_save_path)

        # 无参数更新逻辑
        new_full_params = set_params.copy()

        # 结果入库
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=[img_save_path],
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        logging.info(f"测量完成，参数： {new_full_params}")

    except Exception as e:
        err_msg = f"XEB测量异常：{str(e)}"
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
    get_xeb_hdf5_res(cli_args)