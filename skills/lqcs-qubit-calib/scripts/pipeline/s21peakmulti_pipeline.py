# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################


"""Multi-qubit S21PEAKMULTI spectrum measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
        python -m skills.lqcs-qubit-calib.scripts.pipeline.s21peakmulti_pipeline -q q1ld4 -fs 6.5 -fe 6.8 -r 0.0008 -s ./tmp -u True -c 0.4
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
import json

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
from analysis.inception import nns21peakmulti, s21peakmulti
from analysis.visualization import plot_nns21peakmulti, plot_s21peakmulti

from analysis.update import s21peakmulti_update

DEFAULT_SAVE_FOLDER = './tmp'
CONFIG_PATH = "skills/lqcs-qubit-calib/scripts/pipeline/s21peakmulti_init_freq.json"

# 加载比特基准频率配置
try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        base_freq_dict = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"配置文件不存在，请检查路径: {CONFIG_PATH}")



def parse_args():
    parser = argparse.ArgumentParser(description="Multi Qubit S21MULTI Measurement Pipeline (UI storage sync enabled)")
    # 被测比特列表
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld4"],
                        help="Target qubit name list, default: q1ld4")
    # 扫描起始频率
    parser.add_argument("--freq-start", "-fs", type=float, default=6.5,
                        help="Scan start frequency (GHz)")
    # 扫描终止频率
    parser.add_argument("--freq-end", "-fe", type=float, default=6.7,
                        help="Scan end frequency (GHz)")
    # 频率步长
    parser.add_argument("--sample-rate", "-r", type=float, default=0.0002,
                        help="Frequency sample step (GHz)")
    # 图片保存目录
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Folder to save spectrum plot image")
    # 是否自动更新参数
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    # 置信度阈值
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")

    return parser.parse_args()



# def llm_analysis(img_save_path):
    # resize更小
    # img_small_path = img_save_path.split('.png')[0] + '_small.png'
    # print("img_small_path: ", img_small_path)

    # with Image.open(img_save_path) as img:
        # w, h = img.size
        # new_w = w // 10
        # new_h = h // 10
        # print("size: ", new_w, new_h)
        # img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        # img_small.save(img_small_path, dpi=(300, 300))

    # test_qubit_spectroscopy_q1_describe(img_small_path)
    # test_qubit_spectroscopy_q2_classify(img_small_path)
    # test_qubit_spectroscopy_q3_reasoning(img_small_path)
    # test_qubit_spectroscopy_q4_assess(img_small_path)
    # test_qubit_spectroscopy_q5_extract(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    # print("\nQubit_Spectroscopy tests passed!")



def get_s21peakmulti_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.S21PEAKMULTI.value
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        qubit_ctrl_client = QubitCtrlClient()
        qname = qubit_name_list[0]
        base_freq = base_freq_dict.get(qname)

        # 组装实验参数
        set_params = {
            "qubits": qubit_name_list,
            "frequency_start": args.freq_start,
            "frequency_end": args.freq_end,
            "frequency_sample_rate": args.sample_rate,
            "fread": base_freq
        }

        # 创建实验记录并生成run_id
        run_record = PipelineResultRecord(
            task_name=task_name,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[S21MULTI] Task started run_id={run_id[:8]}")

        # 硬件采集数据
        data_id = qubit_ctrl_client.run(
            CtrlTaskName.S21PEAKMULTI,
            qubits=qubit_name_list,
            frequency_start=args.freq_start,
            frequency_end=args.freq_end,
            frequency_sample_rate=args.sample_rate
        )
        print("141---------", data_id)

        # 读取解析后原始数据
        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 写入原始数据到存储
        store.update_run(run_id=run_id, raw_data_id=data_id, raw_data=raw_data)

        # 数据分析
        analysis_result = s21peakmulti(raw_data)
        print("150---", analysis_result)

        # 绘制频谱图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/{CtrlTaskName.S21PEAKMULTI.value}_{pure_name}_{run_id}.png'
        plot_s21peakmulti(raw_data, analysis_result, save_path=img_save_path)

        # =========== 接入大模型分析图片 ===========
        # llm_analysis(img_save_path)

        new_full_params = set_params.copy()
        update_map = {}

        # 开启自动更新则执行参数更新
        if args.update:

            update_map = s21peakmulti_update(
                results=analysis_result,
                conf_threshold=args.confidence,
                qubit_name_list=qubit_name_list,
                base_freq_dict=base_freq_dict
            )
            # 更新参数
            for q, info in update_map.items():
                new_value = info["fread_star"]

                qubit_ctrl_client.update_param(
                    qname=q,
                    task_type=CtrlTaskName.S21PEAKMULTI,
                    values=str(new_value)
                )

        # 更新最终参数
        if update_map:
            new_full_params["fread_star"] = update_map

        # 完成任务，写结果到存储
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=[img_save_path],
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        logging.info(f"测量完成，最终参数： {new_full_params}")

    except Exception as e:
        err_msg = f"测量异常：{str(e)}"
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
    get_s21peakmulti_hdf5_res(cli_args)