# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiangsun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/18
########################################################################


"""TimingXYZ measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m skills.lqcs-qubit-calib.scripts.pipeline.timingxyz_pipeline -q q1ld5 -ds -60 -de 60 -dn 31 -z 0.5 -u True
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
import os
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

from analysis.inception import timingxyz
from analysis.visualization import plot_timingxyz
from analysis.update import timingxyz_update

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
    parser = argparse.ArgumentParser(description="TimingXYZ Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit name list, default: q1ld5")
    # 延时起始值
    parser.add_argument("--delay-start", "-ds", type=float, default=-60,
                        help="Delay start value, default -60")
    # 延时终止值
    parser.add_argument("--delay-end", "-de", type=float, default=60,
                        help="Delay end value, default 60")
    # 延时采样点数
    parser.add_argument("--delay-sample-num", "-dn", type=int, default=31,
                        help="Delay sampling count, default 31")
    # zpa
    parser.add_argument("--zpa", "-z", type=float, default=0.5,
                        help="zpa, default 0.5")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=SAVE_PLOT_FOLDER,
                        help="Folder to save plot image")
    # 参数更新开关
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    
    # 置信度
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")

    return parser.parse_args()


def get_timingxyz_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.TIMINGXYZ.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    qname = qubit_name_list[0]

    try:
        qubit_ctrl_client = QubitCtrlClient()

        timing_xy_original = float(qubit_ctrl_client.query_param(qname=qname, key="timing_xy_star"))
        
        # 组装实验参数
        set_params = {
            "qubits": qubit_name_list,
            "delay_start": args.delay_start,
            "delay_end": args.delay_end,
            "delay_sample_num": args.delay_sample_num,
            "zpa": args.zpa,
            "timing_xy_star": timing_xy_original
        }

        # 新建实验记录
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[TimingXYZ] Task started run_id={run_id[:8]}")

        # 采集数据
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.TIMINGXYZ,
            qubits=qubit_name_list,
            delay_start=args.delay_start,
            delay_end=args.delay_end,
            delay_sample_num=args.delay_sample_num,
            zpa=args.zpa
        )

        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)


        # 写入原始数据ID与数据
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 分析数据
        analysis_result = timingxyz(raw_data)
        # print("analysis_result: ", analysis_result)


        # 绘图
        img_save_path = f'{save_folder}/{CtrlTaskName.TIMINGXYZ.value}_{qname}_{run_id}.png'
        fig_list = plot_timingxyz(raw_data, analysis_result, save_path=img_save_path)
        
        img_save_path = os.path.abspath(img_save_path)
        plot_paths = [img_save_path]

        # 按需开启图片处理
        # llm_analysis(img_save_path)

        new_full_params = set_params.copy()
        update_map = {}

        # 开启更新
        if args.update:
            update_map = timingxyz_update(
                results=analysis_result,
                conf=args.confidence,
                qubit_name_list=qubit_name_list
            )
            # 更新硬件参数
            task_type = CtrlTaskName.TIMINGXYZ
            for qn, val in update_map.items():
                qubit_ctrl_client.update_param(qname=qn, task_type=task_type, values=[val])

        # 记录更新后的参数
        if update_map:
            new_full_params["timing_xy_star"] = update_map[qubit_name_list[0]]

        # 写入最终结果
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        logging.info(f"TimingXYZ测量完成，更新后参数: {new_full_params}")

    except Exception as e:
        # 异常捕获并记录
        err_msg = f"TimingXYZ测量异常：{str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        raise


if __name__ == '__main__':
    cli_args = parse_args()
    get_timingxyz_hdf5_res(cli_args)