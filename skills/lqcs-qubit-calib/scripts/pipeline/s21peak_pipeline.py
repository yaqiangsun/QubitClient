# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/11
########################################################################


"""Real s21multi measurement pipeline, write data to storage for web UI real-time display
Usage:
    1. Start UI server first: qubitclient ui start
    2. cmd params example:
            python -m resources.lqcs.pipeline.s21peak_pipeline -q q3lu7 -b 0.01 -n 150 -s ./tmp -u True -c 0.6
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
from analysis.inception import s21
from analysis.visualization import plot_s21

DEFAULT_SAVE_FOLDER = './tmp'
TASK_CTRL_TYPE = CtrlTaskName.S21


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="S21 Multi Spectrum Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit name list, default: q3lu7")
    parser.add_argument("--fread", "-f", type=float, default=None,
                        help="Manual readout frequency (GHz). Auto query hardware if not set.")
    parser.add_argument("--bandwidth", "-b", type=float, default=0.005,
                        help="Frequency half bandwidth (GHz), default 0.005")
    parser.add_argument("--samples", "-n", type=int, default=200,
                        help="Number of frequency sampling points, default 200")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Folder to save spectrum plot image")

    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update by analysis")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="update by confidence threshold")
    return parser.parse_args()


def init_storage() -> PipelineResultStore:
    """初始化存储实例"""
    return PipelineResultStore(backend=StorageBackend.LOCAL)


def get_readout_freq(ctrl_client: QubitCtrlClient, qubit_list: list, manual_freq: float) -> float:
    """获取中心频率：优先手动值，无则查询硬件"""
    if manual_freq is not None:
        return manual_freq
    first_q = qubit_list[0]
    freq_ret = ctrl_client.query_param(qname=first_q, key="fread_star")
    return float(freq_ret[0]["text"])


def parse_analysis_result(raw_result: dict):
    """统一解析分析结果"""
    if not isinstance(raw_result, dict):
        return raw_result
    if "results" in raw_result:
        return raw_result["results"]
    elif "result" in raw_result:
        return raw_result["result"]
    return raw_result


def update_qubit_params(
    ctrl_client: QubitCtrlClient,
    qubit_list: list,
    analysis_data,
    conf_threshold: float,
    set_params: dict
) -> dict:
    """根据分析结果与置信度更新量子硬件参数"""
    new_params = set_params.copy()
    if not analysis_data:
        return new_params

    for result in analysis_data:
        print("----------result.keys(): ", result.keys())
        confs_list = result.get("confs", [])
        freqs_list = result.get("freqs_list", [])

        for idx in range(len(qubit_list)):
            if idx >= len(freqs_list) or idx >= len(confs_list):
                continue
            freqs = freqs_list[idx]
            cur_confs = confs_list[idx]
            curr_q = qubit_list[idx]

            if not len(freqs) or not len(cur_confs):
                continue

            updated_freq = str(freqs[0])
            cur_conf = float(cur_confs[0])

            if cur_conf > conf_threshold:
                ctrl_client.update_param(
                    qname=curr_q,
                    task_type=TASK_CTRL_TYPE,
                    values=updated_freq
                )
                new_params["frequency_center"] = float(updated_freq)
    return new_params


def handle_pipeline_exception(store: PipelineResultStore, run_id, exc: Exception):
    """通用流水线异常处理"""
    err_msg = f"测量异常：{str(exc)}"
    if run_id:
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
    print(f"任务失败 run_id={run_id[:8] if run_id else ''} 错误：{err_msg}")
    raise


def collect_raw_data(ctrl_client: QubitCtrlClient, params: dict) -> dict:
    """采集硬件原始数据"""
    data = ctrl_client.run(
        TASK_CTRL_TYPE,
        qubits=params["qubits"],
        frequency_center=params["frequency_center"],
        frequency_half_bandwidth=params["frequency_half_bandwidth"],
        frequency_sample_num=params["frequency_sample_num"]
    )
    data_id = data[0]["text"]
    raw_data_text = ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
    raw_data = json.loads(raw_data_text[0]["text"])
    return {"data_id": data_id, "raw_data": raw_data}


def draw_spectrum_img(raw_data, analysis_res, save_dir: str, qubit_name: str) -> str:
    """绘制频谱图，返回图片路径"""
    img_path = f'{save_dir}/s21peak_{qubit_name}.png'
    plot_s21(raw_data, analysis_res, save_path=img_path)
    return img_path


# def llm_image_analysis(img_path: str):
#     """大模型图片分析逻辑"""
#     img_small_path = img_path.split('.png')[0] + '_small.png'
#     print("img_small_path: ", img_small_path)

#     with Image.open(img_path) as img:
#         w, h = img.size
#         new_w = w // 10
#         new_h = h // 10
#         print("size: ", new_w, new_h)
#         img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
#         img_small.save(img_small_path, dpi=(300, 300))

#     test_qubit_spectroscopy_q1_describe(img_small_path)
#     test_qubit_spectroscopy_q2_classify(img_small_path)
#     test_qubit_spectroscopy_q3_reasoning(img_small_path)
#     test_qubit_spectroscopy_q4_assess(img_small_path)
#     test_qubit_spectroscopy_q5_extract(img_small_path)
#     test_qubit_spectroscopy_q6_status(img_small_path)
#     print("\nQubit_Spectroscopy tests passed!")


def pipeline_main_logic(args):
    """S21 测量流水线主流程"""
    store = init_storage()
    qubit_name_list = args.qubits
    save_folder = args.save_folder
    run_id = None

    try:
        # 初始化客户端
        qubit_ctrl_client = QubitCtrlClient()
        fread = get_readout_freq(qubit_ctrl_client, qubit_name_list, args.fread)
        set_params = {
            "qubits": qubit_name_list,
            "frequency_half_bandwidth": args.bandwidth,
            "frequency_sample_num": args.samples,
            "frequency_center": fread
        }

        # 创建实验记录
        run_record = PipelineResultRecord(
            task_name=CtrlTaskName.S21.value,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[S21] Task started run_id={run_id[:8]}")

        # 采集原始数据
        data_package = collect_raw_data(qubit_ctrl_client, set_params)
        raw_data = data_package["raw_data"]
        data_id = data_package["data_id"]

        # 原始数据入库
        store.update_run(
            run_id=run_id,
            raw_data_id=data_id,
            raw_data=raw_data
        )

        # 数据分析
        analysis_result = s21(raw_data)
        analysis_data = parse_analysis_result(analysis_result)

        # 绘图
        first_qubit = qubit_name_list[0]
        img_save_path = draw_spectrum_img(raw_data, analysis_result, save_folder, first_qubit)

        # 图片大模型分析
        # llm_image_analysis(img_save_path)

        # 更新参数
        new_full_params = set_params.copy()
        if args.update:
            new_full_params = update_qubit_params(
                ctrl_client=qubit_ctrl_client,
                qubit_list=qubit_name_list,
                analysis_data=analysis_data,
                conf_threshold=args.confidence,
                set_params=set_params
            )

        # 最终结果入库
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=[img_save_path],
            completed_at=datetime.now(),
            new_params=new_full_params
        )
        print(f"测量完成，更新： {new_full_params}")

    except Exception as e:
        handle_pipeline_exception(store, run_id, e)


if __name__ == '__main__':
    cli_args = parse_args()
    pipeline_main_logic(cli_args)